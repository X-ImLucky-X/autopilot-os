import re

from tools.browser_tools import search_web


def clean_research_query(task: str):

    # Remove email instructions
    task = re.sub(
        r"email me.*",
        "",
        task,
        flags=re.IGNORECASE
    )

    # Remove scheduling instructions
    task = re.sub(
        r"schedule.*",
        "",
        task,
        flags=re.IGNORECASE
    )

    # Cleanup commas/spaces
    task = task.strip(" ,.")

    return task


def execute_task(task: str):

    print("\n========================")
    print("EXECUTOR STARTED")
    print("========================")

    # Extract only research intent
    research_query = clean_research_query(
        task
    )

    print(
        f"\nClean Research Query: {research_query}"
    )

    search_results = search_web(
        research_query
    )

    print("\nSEARCH RESULTS:")
    print(search_results)

    combined_content = search_results.get(
        "text",
        ""
    )

    links = search_results.get(
        "links",
        []
    )

    print("\nLINKS FOUND:")
    print(links)

    print("\nCONTENT LENGTH:")
    print(len(combined_content))

    print("\nCONTENT PREVIEW:")
    print(combined_content[:1000])

    if not combined_content.strip():

        return """
No content could be extracted from web search.
"""

    return combined_content[:12000]