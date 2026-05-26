from playwright.sync_api import sync_playwright


def search_web(query: str):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )

        page = browser.new_page()

        page.goto("https://duckduckgo.com")

        page.fill('input[name="q"]', query)

        page.keyboard.press("Enter")

        page.wait_for_load_state("networkidle")

        results = page.locator('[data-testid="result"]')

        extracted_text = ""

        count = min(results.count(), 5)

        for i in range(count):

            result = results.nth(i)

            extracted_text += result.inner_text() + "\n\n"

        browser.close()

        return extracted_text