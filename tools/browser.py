import webbrowser
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def open_website(url: str) -> str:
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    return f"Opened {url} in your browser."


def search_google(query: str) -> str:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Opened a Google search for '{query}'."


def search_youtube(query: str) -> str:
    url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Opened a YouTube search for '{query}'."


def search_github(query: str) -> str:
    url = f"https://github.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Opened a GitHub search for '{query}'."


def read_webpage(url: str) -> str:
    """
    Fetches a webpage and extracts its main readable text
    (no visible browser opens — this happens invisibly in the background).
    """
    if not url.startswith("http"):
        url = "https://" + url

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except Exception as e:
        return f"Couldn't fetch {url}: {e}"

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    lines = [line for line in text.split("\n") if line]
    cleaned = "\n".join(lines)

    if len(cleaned) > 6000:
        cleaned = cleaned[:6000] + "\n...[content truncated]"

    return cleaned