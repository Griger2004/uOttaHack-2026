"""
Business logic services for the fake news detection pipeline.

The pipeline consists of three agents:
1. Reader - Extracts the core claim from an article
2. Researcher - Searches and scrapes sources to verify the claim
3. Judge - Compares the article with sources and renders a verdict
"""

from .reader import ReaderService
from .researcher import ResearcherService
from .judge import JudgeService
from .pipeline import VerificationPipeline

__all__ = [
    "ReaderService",
    "ResearcherService",
    "JudgeService",
    "VerificationPipeline",
]
