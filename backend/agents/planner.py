import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_plan(task: str):

    prompt = f"""
    You are an AI planning agent.

    Convert the user's task into clear execution steps.

    Task:
    {task}

    Return steps in numbered format.
    """

    response = model.generate_content(prompt)

    return response.text