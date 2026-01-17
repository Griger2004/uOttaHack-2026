"""
The Judge Agent - Step 3 of the verification pipeline.
Compares the article with sources and renders a verdict.
"""

import json
from datetime import datetime
from schemas.verify import JudgmentResult
from clients.gemini import gemini_client


class JudgeService:
    """
    Service for judging articles against scraped sources.
    Uses Gemini to analyze and compare content.
    """

    # 2. UPDATE THE TEMPLATE TO INCLUDE CURRENT DATE
    PROMPT_TEMPLATE = """You are a fact-checking judge. 
Current Date: {current_date}

Compare the ORIGINAL ARTICLE with information from TRUSTED SOURCES below.
Analyze whether the claims in the original article are supported by the trusted sources.

ORIGINAL ARTICLE:
{original_article}

TRUSTED SOURCES:
{scraped_sources}

Return your analysis as a JSON object with exactly these fields:
- trust_score: An integer from 0 to 100 (0 = completely fake, 100 = completely true)
- verdict: One of "Fake", "True", or "Unverified"
- reasoning: A single sentence explaining your verdict

Output ONLY the JSON object, no other text."""

    DEFAULT_RESULT = JudgmentResult(
        trust_score=50,
        verdict="Unverified",
        reasoning="Unable to complete verification due to processing error.",
    )

    def judge_article(
        self,
        original_article: str,
        scraped_sources: str,
    ) -> JudgmentResult:
        """
        Judge an article by comparing it with scraped sources.

        Args:
            original_article: The original article text.
            scraped_sources: Combined text from scraped sources.

        Returns:
            JudgmentResult containing trust_score, verdict, and reasoning.
        """
        prompt = self.PROMPT_TEMPLATE.format(
            current_date=datetime.now().strftime("%Y-%m-%d"),  # <--- Add this line
            original_article=original_article,
            scraped_sources=scraped_sources,
        )

        try:
            response_text = gemini_client.generate(prompt)

            # Extract JSON from response (handle markdown code blocks)
            json_text = self._extract_json(response_text)

            # Parse JSON
            result_dict = json.loads(json_text)

            # Validate and return
            return JudgmentResult(
                trust_score=result_dict["trust_score"],
                verdict=result_dict["verdict"],
                reasoning=result_dict["reasoning"],
            )

        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from Gemini: {e}")
            return self.DEFAULT_RESULT
        except KeyError as e:
            print(f"Missing required field in Gemini response: {e}")
            return self.DEFAULT_RESULT
        except Exception as e:
            print(f"Error judging article: {e}")
            return JudgmentResult(
                trust_score=50,
                verdict="Unverified",
                reasoning=f"Unable to complete verification: {str(e)}",
            )

    def _extract_json(self, text: str) -> str:
        """
        Extract JSON from text that might be wrapped in markdown code blocks.

        Args:
            text: The text potentially containing JSON.

        Returns:
            The extracted JSON string.
        """
        if "```json" in text:
            return text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text.strip()


# Singleton instance
judge_service = JudgeService()
