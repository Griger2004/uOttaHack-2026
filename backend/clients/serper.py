"""
Serper API client for Google Search.
"""

from typing import List
import requests
from config import settings


class SerperClient:
    """Client for searching Google via Serper API."""

    def __init__(self):
        """Initialize the Serper client."""
        self.endpoint = settings.serper_endpoint
        self.api_key = settings.serper_api_key
        self.timeout = settings.request_timeout

    def search(self, query: str, num_results: int = None) -> List[dict]:
        """
        Search Google using Serper API and return rich context for each result.

        Args:
            query: The search query.
            num_results: Number of results to return (default from settings).

        Returns:
            List of dicts containing link, title, snippet, and date for each result.
        """
        if num_results is None:
            num_results = settings.search_results_limit

        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "q": query,
            "num": num_results,
        }

        try:
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()

            # Extract rich context from organic results
            results = []
            if "organic" in data:
                for result in data["organic"][:num_results]:
                    if "link" in result:
                        results.append({
                            "link": result["link"],
                            "title": result.get("title", ""),
                            "snippet": result.get("snippet", ""),
                            "date": result.get("date", "Unknown date"),
                        })

            return results

        except requests.RequestException as e:
            print(f"Error searching Google: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in Serper search: {e}")
            return []


# Singleton instance for reuse
serper_client = SerperClient()
