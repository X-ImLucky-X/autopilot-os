from ollama_client import generate_response


def summarize_content(content: str):

    prompt = f"""
    Summarize the following content.

    Keep it:
    - short
    - informative
    - readable

    Content:
    {content[:4000]}
    """

    return generate_response(prompt)