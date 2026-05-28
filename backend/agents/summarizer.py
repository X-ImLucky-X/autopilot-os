from ollama_client import generate_response


def summarize_content(content: str):

    # Fallback if empty content
    if not content or len(content.strip()) < 100:

        return """
# No Research Content Found

PilotOS could not extract enough article content to generate a proper summary.

Possible reasons:
- website blocked scraping
- article content unavailable
- network issue
- extraction failed
"""

    prompt = f"""
You are an AI research assistant.

Analyze the following research content and generate a professional markdown summary.

Rules:
- DO NOT ask for more content
- DO NOT say "please provide content"
- ALWAYS generate a final summary
- Use markdown formatting
- Use headings and bullet points
- Focus on important insights only
- Make the summary clean and professional

Research Content:

{content[:5000]}


Output Format Example:

# NVIDIA AI News Summary

## Key Highlights
- Point 1
- Point 2

## Important Developments
- Point 1
- Point 2

## Overall Insight
Short final insight paragraph.
"""

    response = generate_response(prompt)

    # Safety fallback
    if (
        "please provide" in response.lower()
        or len(response.strip()) < 20
    ):

        return """
# Research Summary

PilotOS successfully completed the research task, but the AI model returned an incomplete response.

Try:
- improving article extraction
- using a different Ollama model
- refining the search query
"""

    return response