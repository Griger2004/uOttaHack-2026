"""
Pydantic models for the verification endpoint.
"""

from typing import Optional
from pydantic import BaseModel, Field


class VerifyRequest(BaseModel):
    """Request model for article verification."""

    article_text: str = Field(
        ...,
        min_length=10,
        description="The article text to verify for fake news",
        examples=["Scientists discover new species in the Amazon rainforest..."],
    )


class VerifyResponse(BaseModel):
    """Response model for article verification."""

    trust_score: int = Field(
        ...,
        ge=0,
        le=100,
        description="Trust score from 0 (completely fake) to 100 (completely true)",
    )
    verdict: str = Field(
        ...,
        description="Verdict: 'Fake', 'True', or 'Unverified'",
    )
    reasoning: str = Field(
        ...,
        description="Single sentence explaining the verdict",
    )
    search_query: Optional[str] = Field(
        default=None,
        description="The search query used to verify the claim",
    )
    sources_checked: Optional[int] = Field(
        default=None,
        description="Number of sources checked during verification",
    )


class JudgmentResult(BaseModel):
    """Internal model for the judgment step result."""

    trust_score: int
    verdict: str
    reasoning: str
