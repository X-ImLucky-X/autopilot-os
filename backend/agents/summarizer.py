import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


def summarize_content(content: str):

    try:

        prompt = f"""
        Summarize the following web search results.

        Keep it:
        - short
        - informative
        - readable

        Content:
        {content[:4000]}
        """

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Summarization failed: {str(e)}"