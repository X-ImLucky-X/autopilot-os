import requests
import feedparser

from bs4 import BeautifulSoup


def search_web(query: str):

    all_content = ""

    links = []

    try:

        rss_url = (
            "https://news.google.com/rss/search?q="
            + query.replace(" ", "+")
        )

        feed = feedparser.parse(rss_url)

        entries = feed.entries[:5]

        print(f"Found {len(entries)} news results")

        for entry in entries:
            
            try:

                # Real article URL
                link = entry.get(
                    "source", {}
                ).get("href")

                # Fallback
                if not link:

                    link = entry.link

                print(f"Link Found: {link}")

                if link:

                    links.append(link)

            except Exception as e:

                print(
                    f"RSS parsing failed: {e}"
                )

    except Exception as e:

        print(f"RSS Search Failed: {e}")

    # Extract articles
    for link in links[:3]:

        article = extract_article_content(link)

        if article and len(article) > 500:

            all_content += (
                f"\n\nSOURCE: {link}\n\n"
            )

            all_content += article

    return {

        "text": all_content,

        "links": links
    }


def extract_article_content(url: str):

    try:

        headers = {

            "User-Agent":
            (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/122.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove junk
        for tag in soup([
            "script",
            "style",
            "nav",
            "footer",
            "header",
            "aside"
        ]):

            tag.decompose()

        text = soup.get_text(
            separator=" "
        )

        text = " ".join(
            text.split()
        )

        return text[:5000]

    except Exception as e:

        print(
            f"Failed extracting {url}: {e}"
        )

        return ""