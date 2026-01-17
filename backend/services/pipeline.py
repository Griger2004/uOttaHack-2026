"""
Verification Pipeline - Orchestrates the 3-step fake news detection process.
"""

from schemas.verify import VerifyResponse
from .reader import reader_service
from .researcher import researcher_service
from .judge import judge_service


class VerificationPipeline:
    """
    Orchestrates the complete verification pipeline:
    1. Reader: Extract core claim
    2. Researcher: Search and scrape sources
    3. Judge: Compare and render verdict
    """

    def __init__(self):
        """Initialize the pipeline with service dependencies."""
        self.reader = reader_service
        self.researcher = researcher_service
        self.judge = judge_service

    async def verify(self, article_text: str) -> VerifyResponse:
        """
        Execute the full verification pipeline.

        Args:
            article_text: The article text to verify.

        Returns:
            VerifyResponse containing the verification results.
        """
        # Step 1: Extract core claim and generate search query
        print("Step 1: Extracting core claim...")
        search_query = self.reader.extract_core_claim(article_text)
        print(f"Search query: {search_query}")

        # Step 2: Research the claim
        print("Step 2: Researching claim...")
        scraped_sources, sources_count = self.researcher.research_claim(search_query)
        print(f"Scraped {len(scraped_sources)} characters from {sources_count} sources")

        # Step 3: Judge the article
        print("Step 3: Judging article...")
        judgment = self.judge.judge_article(article_text, scraped_sources)

        # Build and return response
        return VerifyResponse(
            trust_score=judgment.trust_score,
            verdict=judgment.verdict,
            reasoning=judgment.reasoning,
            search_query=search_query,
            sources_checked=sources_count,
        )


# Singleton instance
verification_pipeline = VerificationPipeline()
