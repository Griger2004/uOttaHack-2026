# Agentic Fake News Detector - Backend

FastAPI backend for detecting fake news using a 3-step AI-powered pipeline.

## Architecture

1. **The Reader (Gemini)**: Extracts core claim from article
2. **The Researcher (Serper + Yellowcake)**: Searches Google and scrapes trusted sources
3. **The Judge (Gemini)**: Compares claims and returns verdict

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables

Create a `.env` file (or export them):

```bash
export GEMINI_API_KEY="your_gemini_api_key"
export YELLOWCAKE_API_KEY="your_yellowcake_api_key"
export SERPER_API_KEY="your_serper_api_key"
```

### 3. Run the Server

```bash
uvicorn main:app --reload
```

Server will start at `http://localhost:8000`

## API Endpoints

### POST `/verify`

Verify an article for fake news.

**Request Body:**
```json
{
  "article_text": "Pope Francis announced today that he is buying the New York Knicks..."
}
```

**Response:**
```json
{
  "trust_score": 15,
  "verdict": "Fake",
  "reasoning": "No credible news sources confirm this claim, and it contradicts Vatican policies.",
  "search_query": "Pope Francis buying New York Knicks",
  "sources_checked": 3
}
```

### GET `/`

Health check endpoint.

## Tech Stack

- FastAPI
- Pydantic
- Google Gemini 1.5 Flash
- Serper API (Google Search)
- Yellowcake API (Web Scraping)
- Requests

## Development

View API docs at: `http://localhost:8000/docs`
