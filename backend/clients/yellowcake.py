"""
Yellowcake API client for web scraping.
Updated for streaming (SSE) response handling.
"""

import json
import requests
from typing import Optional
from config import settings


class YellowcakeClient:
    """Client for scraping web content via Yellowcake API."""

    def __init__(self):
        self.endpoint = settings.yellowcake_endpoint
        self.api_key = settings.yellowcake_api_key
        self.timeout = settings.request_timeout

    def scrape(self, url: str) -> Optional[str]:
        """
        Scrape a URL and extract content using Yellowcake's Stream API.
        """
        # --- FIX 3: Correct Header Name (X-API-Key) ---
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

        # Yellowcake requires a 'prompt' field
        payload = {
            "url": url,
            "prompt": "Extract the main article content, ignoring navigation and footers.",
        }

        try:
            # We use stream=True to handle the SSE response
            response = requests.post(
                self.endpoint,
                headers=headers,
                json=payload,
                timeout=self.timeout,
                stream=True,
            )
            response.raise_for_status()

            # --- FIX 4: Parse the SSE Stream ---
            # Yellowcake sends data in chunks. We need to find the "complete" event.
            final_data = None

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")

                    # Look for the final data payload
                    if decoded_line.startswith("data:"):
                        try:
                            json_str = decoded_line.replace("data: ", "")
                            data = json.loads(json_str)

                            # If this is the final payload, it will have 'data' or 'content'
                            if "data" in data and isinstance(data["data"], list):
                                # Yellowcake returns a list of extractions. We join them.
                                parts = []
                                for item in data["data"]:
                                    # Depending on prompt, keys vary. We dump values.
                                    parts.extend(item.values())
                                final_data = "\n".join(parts)

                        except json.JSONDecodeError:
                            continue

            return final_data

        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error scraping {url}: {e}")
            return None


# Singleton instance
yellowcake_client = YellowcakeClient()
