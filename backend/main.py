import os
import json
from typing import Optional, List, Dict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import requests


# Initialize FastAPI app
app = FastAPI(title="Agentic Fake News Detector")

# Configure CORS for hackathon demo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load API keys from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YELLOWCAKE_API_KEY = os.getenv("YELLOWCAKE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


# Pydantic models
class VerifyRequest(BaseModel):
    article_text: str


class VerifyResponse(BaseModel):
    trust_score: int
    verdict: str
    reasoning: str
    search_query: Optional[str] = None
    sources_checked: Optional[int] = None


# Helper function: Search Google using Serper API
def search_google(query: str) -> List[str]:
    """
    Search Google using Serper API and return top 3 URLs.
    """
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": query,
        "num": 3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract URLs from organic results
        urls = []
        if "organic" in data:
            for result in data["organic"][:3]:
                if "link" in result:
                    urls.append(result["link"])
        
        return urls
    except Exception as e:
        print(f"Error searching Google: {e}")
        return []


# Helper function: Scrape content using Yellowcake API
def scrape_with_yellowcake(url: str) -> Optional[str]:
    """
    Scrape a URL using Yellowcake API and return the main body text.
    Returns None if scraping fails.
    """
    api_url = "https://api.yellowcake.ai/v1/extract"
    headers = {
        "Authorization": f"Bearer {YELLOWCAKE_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "url": url,
        "extract_content": True
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Extract main content from response
        # Adjust based on actual Yellowcake response format
        if "content" in data:
            return data["content"]
        elif "text" in data:
            return data["text"]
        elif "body" in data:
            return data["body"]
        
        return None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


# Step 1: The Reader - Extract core claim using Gemini
def extract_core_claim(article_text: str) -> str:
    """
    Use Gemini to extract the core claim from the article and generate a search query.
    """
    prompt = f"""You are a fact-checking assistant. Read the following article and extract the MAIN CLAIM that should be verified.

Output ONLY a concise search query (2-8 words) that would help verify this claim on Google. Do not include any explanation, quotes, or extra text.

Article:
{article_text}

Search Query:"""
    
    try:
        response = model.generate_content(prompt)
        search_query = response.text.strip()
        # Remove any quotes that might be in the response
        search_query = search_query.replace('"', '').replace("'", '')
        return search_query
    except Exception as e:
        print(f"Error extracting core claim: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract core claim: {str(e)}")


# Step 2: The Researcher - Search and scrape trusted sources
def research_claim(search_query: str) -> str:
    """
    Search Google and scrape content from top 3 URLs.
    Returns combined text from all successfully scraped sources.
    """
    # Get top 3 URLs from Google
    urls = search_google(search_query)
    
    if not urls:
        return "No sources found for verification."
    
    # Scrape each URL
    scraped_contents = []
    for url in urls:
        content = scrape_with_yellowcake(url)
        if content:
            scraped_contents.append(f"Source: {url}\n{content[:2000]}")  # Limit to first 2000 chars per source
    
    if not scraped_contents:
        return "Failed to scrape any sources for verification."
    
    return "\n\n---\n\n".join(scraped_contents)


# Step 3: The Judge - Compare and verdict using Gemini
def judge_article(original_article: str, scraped_sources: str) -> Dict:
    """
    Use Gemini to compare the original article with scraped sources and return a verdict.
    """
    prompt = f"""You are a fact-checking judge. Compare the ORIGINAL ARTICLE with information from TRUSTED SOURCES below.

Analyze whether the claims in the original article are supported by the trusted sources.

ORIGINAL ARTICLE:
{original_article}

TRUSTED SOURCES:
{scraped_sources}

Return your analysis as a JSON object with exactly these fields:
- trust_score: An integer from 0 to 100 (0 = completely fake, 100 = completely true)
- verdict: One of "Fake", "True", or "Unverified"
- reasoning: A single sentence explaining your verdict

Output ONLY the JSON object, no other text."""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response (sometimes Gemini wraps it in markdown)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        # Parse JSON
        result = json.loads(response_text)
        
        # Validate required fields
        if not all(key in result for key in ["trust_score", "verdict", "reasoning"]):
            raise ValueError("Missing required fields in Gemini response")
        
        return result
    except Exception as e:
        print(f"Error judging article: {e}")
        # Return a default response if parsing fails
        return {
            "trust_score": 50,
            "verdict": "Unverified",
            "reasoning": f"Unable to complete verification due to processing error: {str(e)}"
        }


# Main endpoint: POST /verify
@app.post("/verify", response_model=VerifyResponse)
async def verify_article(request: VerifyRequest):
    """
    Main endpoint that executes the 3-step Agentic Fake News Detection pipeline:
    1. The Reader: Extract core claim
    2. The Researcher: Search and scrape sources
    3. The Judge: Compare and verdict
    """
    article_text = request.article_text
    
    if not article_text or len(article_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Article text is too short or empty")
    
    # Step 1: Extract core claim and generate search query
    print("Step 1: Extracting core claim...")
    search_query = extract_core_claim(article_text)
    print(f"Search query: {search_query}")
    
    # Step 2: Research the claim
    print("Step 2: Researching claim...")
    scraped_sources = research_claim(search_query)
    print(f"Scraped {len(scraped_sources)} characters from sources")
    
    # Step 3: Judge the article
    print("Step 3: Judging article...")
    verdict = judge_article(article_text, scraped_sources)
    
    # Return response
    return VerifyResponse(
        trust_score=verdict["trust_score"],
        verdict=verdict["verdict"],
        reasoning=verdict["reasoning"],
        search_query=search_query,
        sources_checked=len(scraped_sources.split("---"))
    )


# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "Agentic Fake News Detector API",
        "status": "online",
        "endpoints": {
            "POST /verify": "Verify an article for fake news"
        }
    }


# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
