from ollama_client import generate_response


def generate_plan(task: str):

    prompt = f"""
    You are an AI planning agent.

    Convert the user's task into clear execution steps.

    Task:
    {task}

    Return concise numbered steps.
    """

    return generate_response(prompt)