"""
The Reader Agent - Step 1 of the verification pipeline.
Extracts the core claim from an article and generates a search query.
"""

from clients.gemini import gemini_client


class ReaderService:
    """
    Service for extracting core claims from articles.
    Uses Gemini to analyze text and generate search queries.
    """

    PROMPT_TEMPLATE = """You are a professional fact-checker. 
        Read the article below and identify the central claim that seems suspicious or requires verification.

        Generate a Google Search query to verify this claim. 
        Crucial: Construct the query to find INDEPENDENT CONFIRMATION or DEBUNKING articles. 
        Prefer keywords like "fact check", "official", "snopes", "reuters", or "hoax".

        Article:
        {article_text}

        Output ONLY the search query string (no quotes):"""

    def extract_core_claim(self, article_text: str) -> str:
        """
        Extract the core claim from an article and generate a search query.

        Args:
            article_text: The full text of the article to analyze.

        Returns:
            A concise search query (2-8 words) to verify the claim.

        Raises:
            Exception: If Gemini fails to generate a response.
        """
        prompt = self.PROMPT_TEMPLATE.format(article_text=article_text)
        print(f"🔍 DEBUG: Generating prompt: {prompt}")
        response = gemini_client.generate(prompt)
        print(f"🔍 DEBUG: Gemini response: {response}")
        # Clean up the response - remove quotes and extra whitespace
        search_query = response.replace('"', "").replace("'", "").strip()
        print(f"🔍 DEBUG: Cleaned search query: {search_query}")

        return search_query


# Singleton instance
reader_service = ReaderService()
