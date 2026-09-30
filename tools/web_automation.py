from playwright.sync_api import sync_playwright
import os


_playwright = None
_browser = None
_page = None
_elements_cache = []

USER_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "browser_profile")


def start_browser() -> str:
    global _browser, _page
    if _browser:
        return "Browser is already open."

    global _playwright
    _playwright = sync_playwright().start()
    _browser = _playwright.chromium.launch_persistent_context(
        USER_DATA_DIR,
        headless=False
    )
    _page = _browser.new_page()
    return "Browser started."


def navigate_browser(url: str) -> str:
    global _page
    if not _page:
        start_browser()
    if not url.startswith("http"):
        url = "https://" + url
    _page.goto(url, wait_until="domcontentloaded")
    return f"Navigated to {url}."


def get_page_elements() -> str:
    """Returns a numbered list of clickable/fillable elements currently visible on the page."""
    global _elements_cache
    if not _page:
        return "No browser open. Call navigate_browser first."

    _elements_cache = []
    elements = _page.query_selector_all("a, button, input, textarea, select")
    lines = []
    for el in elements:
        try:
            if not el.is_visible():
                continue
            tag = el.evaluate("e => e.tagName").lower()
            text = (el.inner_text() or "").strip()[:60]
            placeholder = el.get_attribute("placeholder") or ""
            label = text or placeholder or el.get_attribute("aria-label") or ""
            if not label:
                continue
            _elements_cache.append(el)
            lines.append(f"[{len(_elements_cache) - 1}] <{tag}> {label}")
            if len(_elements_cache) >= 40:
                break
        except Exception:
            continue

    if not lines:
        return "No interactive elements found on this page."
    return "\n".join(lines)


def click_element(index: int) -> str:
    if index < 0 or index >= len(_elements_cache):
        return f"No element at index {index}. Call get_page_elements first to see valid indexes."
    try:
        _elements_cache[index].click()
        return f"Clicked element {index}."
    except Exception as e:
        return f"Couldn't click element {index}: {e}"


def fill_element(index: int, text: str) -> str:
    if index < 0 or index >= len(_elements_cache):
        return f"No element at index {index}. Call get_page_elements first to see valid indexes."
    try:
        _elements_cache[index].fill(text)
        return f"Filled element {index} with '{text}'."
    except Exception as e:
        return f"Couldn't fill element {index}: {e}"


def close_browser() -> str:
    global _playwright, _browser, _page
    if _browser:
        _browser.close()
        _playwright.stop()
        _browser = None
        _page = None
        return "Browser closed."
    return "No browser was open."