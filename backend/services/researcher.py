"""
The Researcher Agent - Step 2 of the verification pipeline.
Searches for sources and scrapes their content.
"""

import asyncio
from typing import List, Tuple
from clients.serper import serper_client
from clients.yellowcake import yellowcake_client
from config import settings


class ResearcherService:
    """
    Service for researching claims by searching and scraping sources.
    """

    async def research_claim(self, search_query: str) -> Tuple[str, int]:
        """
        Research a claim by searching Google and scraping top results in parallel.

        Args:
            search_query: The search query to use.

        Returns:
            Tuple of (combined scraped content, number of sources checked).
        """
        # Get rich context from Google search
        search_results = serper_client.search(search_query)

        if not search_results:
            return "No sources found for verification.", 0

        async def fetch_content(result: dict) -> str:
            """Fetch content for a single result with snippet fallback."""
            link = result["link"]
            title = result["title"]
            snippet = result["snippet"]
            date = result["date"]

            try:
                # Run scrape in a separate thread to avoid blocking
                content = await asyncio.to_thread(yellowcake_client.scrape, link)

                if content:
                    # Scrape succeeded - truncate and return
                    truncated_content = content[: settings.max_content_per_source]
                    return f"Source: {link}\n{truncated_content}"
                else:
                    # Scrape returned empty - use snippet fallback
                    return (
                        f"Source: {link} (Snippet Only)\n"
                        f"Title: {title}\n"
                        f"Date: {date}\n"
                        f"Summary: {snippet}"
                    )
            except Exception:
                # Scrape failed - use snippet fallback
                return (
                    f"Source: {link} (Snippet Only)\n"
                    f"Title: {title}\n"
                    f"Date: {date}\n"
                    f"Summary: {snippet}"
                )

        async def gather_all():
            """Gather content from all sources in parallel."""
            tasks = [fetch_content(result) for result in search_results]
            return await asyncio.gather(*tasks)

        # Run the async gathering
        scraped_contents = await gather_all()

        # Filter out any None results (shouldn't happen with fallback, but just in case)
        valid_contents = [c for c in scraped_contents if c]

        if not valid_contents:
            return "Failed to scrape any sources for verification.", 0

        combined_content = "\n\n---\n\n".join(valid_contents)
        return combined_content, len(valid_contents)

    def get_sources(self, search_query: str) -> List[str]:
        """
        Get source URLs for a search query without scraping.

        Args:
            search_query: The search query to use.

        Returns:
            List of source URLs.
        """
        # Extract just the links from the rich context
        results = serper_client.search(search_query)
        return [r["link"] for r in results]


# Singleton instance
researcher_service = ResearcherService()
