import requests
from tavily import TavilyClient
from config import TAVILY_API_KEY, SERPER_API_KEY

_tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY else None


def _search_tavily(query: str) -> str:
    response = _tavily_client.search(query=query, max_results=5)
    results = response.get("results", [])
    if not results:
        return "No results found."

    lines = []
    for r in results:
        lines.append(f"- {r['title']}: {r['content'][:300]} ({r['url']})")
    return "\n".join(lines)


def _search_serper(query: str) -> str:
    response = requests.post(
        "https://google.serper.dev/search",
        headers={"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"},
        json={"q": query},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    organic = data.get("organic", [])
    if not organic:
        return "No results found."

    lines = []
    for r in organic[:5]:
        title = r.get("title", "")
        snippet = r.get("snippet", "")
        link = r.get("link", "")
        lines.append(f"- {title}: {snippet} ({link})")
    return "\n".join(lines)


def web_search(query: str) -> str:
    try:
        return _search_tavily(query)
    except Exception as e:
        print(f"[web_search] Tavily failed ({e}), falling back to Serper...")
        try:
            return _search_serper(query)
        except Exception as e2:
            return f"Search failed on both providers. ({e2})"

def research_topic(topic: str, angles: list[str] = None) -> str:
    if not angles:
        angles = [topic, f"{topic} comparison"]

    combined = []
    for angle in angles[:2]:  # reduced further to 2
        result = web_search(angle)
        if len(result) > 500:
            result = result[:500] + "...[truncated]"
        combined.append(f"=== Search: '{angle}' ===\n{result}\n")

    return "\n".join(combined)