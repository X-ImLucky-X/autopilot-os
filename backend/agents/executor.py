from tools.browser_tools import search_web


def execute_task(task: str):

    result = search_web(task)

    return result[:5000]