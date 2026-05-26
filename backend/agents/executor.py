from tools.browser_tools import (
    search_web,
    extract_article_content
)


def execute_task(task: str):

    search_results = search_web(task)

    combined_content = search_results["text"]

    links = search_results["links"]

    for link in links:

        try:

            article_content = extract_article_content(link)

            combined_content += "\n\n" + article_content

        except Exception as e:

            print(f"Failed to extract {link}: {e}")

    return combined_content[:12000]