"""
Verification endpoint router.
Handles the /verify endpoint for fake news detection.
"""

from fastapi import APIRouter, HTTPException
from schemas.verify import VerifyRequest, VerifyResponse
from services.pipeline import verification_pipeline

router = APIRouter(prefix="/verify", tags=["verification"])


@router.post("", response_model=VerifyResponse)
async def verify_article(request: VerifyRequest) -> VerifyResponse:
    """
    Verify an article for fake news using the 3-step agentic pipeline.

    **Pipeline Steps:**
    1. **The Reader**: Extract the core claim and generate a search query
    2. **The Researcher**: Search Google and scrape top sources
    3. **The Judge**: Compare the article with sources and render a verdict

    **Request Body:**
    - `article_text`: The article text to verify (min 10 characters)

    **Response:**
    - `trust_score`: 0-100 score (0 = fake, 100 = true)
    - `verdict`: "Fake", "True", or "Unverified"
    - `reasoning`: Explanation of the verdict
    - `search_query`: The query used for verification
    - `sources_checked`: Number of sources analyzed
    """
    try:
        return await verification_pipeline.verify(request.article_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {str(e)}",
        )
