from playwright.sync_api import sync_playwright


def search_web(query: str):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.new_page()

        # Open DuckDuckGo
        page.goto("https://duckduckgo.com")

        # Fill search
        page.fill('input[name="q"]', query)

        # Press enter
        page.keyboard.press("Enter")

        # Wait until results load
        page.wait_for_load_state("networkidle")

        # Extract page text
        content = page.locator("body").inner_text()

        browser.close()

        return content