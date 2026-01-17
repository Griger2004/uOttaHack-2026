"""
The Researcher Agent - Step 2 of the verification pipeline.
Searches for sources and scrapes their content.
"""

from typing import List, Tuple
from clients.serper import serper_client
from clients.yellowcake import yellowcake_client
from config import settings


class ResearcherService:
    """
    Service for researching claims by searching and scraping sources.
    """

    def research_claim(self, search_query: str) -> Tuple[str, int]:
        """
        Research a claim by searching Google and scraping top results.

        Args:
            search_query: The search query to use.

        Returns:
            Tuple of (combined scraped content, number of sources checked).
        """
        # Get URLs from Google search
        urls = serper_client.search(search_query)

        if not urls:
            return "No sources found for verification.", 0

        # Scrape each URL
        scraped_contents = []
        for url in urls:
            content = yellowcake_client.scrape(url)
            if content:
                # Limit content length per source
                truncated_content = content[: settings.max_content_per_source]
                scraped_contents.append(f"Source: {url}\n{truncated_content}")

        if not scraped_contents:
            return "Failed to scrape any sources for verification.", 0

        combined_content = "\n\n---\n\n".join(scraped_contents)
        return combined_content, len(scraped_contents)

    def get_sources(self, search_query: str) -> List[str]:
        """
        Get source URLs for a search query without scraping.

        Args:
            search_query: The search query to use.

        Returns:
            List of source URLs.
        """
        return serper_client.search(search_query)


# Singleton instance
researcher_service = ResearcherService()
