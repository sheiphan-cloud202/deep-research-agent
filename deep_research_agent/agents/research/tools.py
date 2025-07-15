import json
import logging

import requests
from strands import tool

from deep_research_agent.common.config import settings

# Configure logging
logging.getLogger("strands").setLevel(logging.INFO)


# Define a websearch tool
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
    """Search the web to get updated information.
    Args:
        keywords (str): The search query keywords.
        region (str): The search region, e.g., 'us-en' for USA with English.
        max_results (int | None): The maximum number of results to return.
    Returns:
        String with search results.
    """
    url = "https://google.serper.dev/search"
    api_key = settings.serper_api_key

    if not api_key:
        return "Error: SERPER_API_KEY environment variable is not set. Please set it to use the websearch tool."

    payload = {"q": keywords}
    if region:
        country = region.split("-")[0]
        lang = region.split("-")[1] if len(region.split("-")) > 1 else ""
        if country:
            payload["gl"] = country
        if lang:
            payload["hl"] = lang
    if max_results:
        payload["num"] = str(max_results)

    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for bad status codes
        results = response.json()
        return str(results) if results else "No results found."
    except requests.exceptions.RequestException as e:
        return f"RequestException: {e}"
    except Exception as e:
        return f"Exception: {e}"
