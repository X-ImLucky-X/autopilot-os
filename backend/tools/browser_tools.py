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
        links = []

        count = min(results.count(), 3)

        for i in range(count):

            result = results.nth(i)

            extracted_text += result.inner_text() + "\n\n"

            try:

                link = result.locator(
                    "a[href^='http']"
                ).first.get_attribute("href")

                if link and link.startswith("http"):

                    links.append(link)

            except:

                pass

        browser.close()

        return {
            "text": extracted_text,
            "links": links
        }


def extract_article_content(url: str):

    try:

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=True
            )

            page = browser.new_page()

            page.goto(
                url,
                timeout=30000
            )

            page.wait_for_load_state("networkidle")

            content = page.locator("body").inner_text()

            browser.close()

            return content[:3000]

    except Exception as e:

        return f"Failed to extract {url}: {str(e)}"