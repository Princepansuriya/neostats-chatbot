import requests
from config.config import WEB_SEARCH_API_KEY

def web_search(query):
    """Perform real-time web search using Tavily."""
    try:
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": WEB_SEARCH_API_KEY,
                "query": query,
                "max_results": 5
            }
        )

        data = response.json()
        results = "\n".join([item["content"] for item in data["results"]])
        return results

    except Exception as e:
        return f"Web search failed: {e}"
