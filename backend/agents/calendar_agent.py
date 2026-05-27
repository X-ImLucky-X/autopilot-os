import json
import re
from datetime import datetime, timedelta

from ollama_client import generate_response


def extract_calendar_details(task: str):

    today = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""
    Today is {today}.

    Extract meeting details from the user request.

    Return ONLY valid JSON.

    Rules:
    - Convert relative dates like "tomorrow" and similar to absolute dates
    - Use 24-hour time format
    - duration_hours should be integer

    Example:

    {{
        "title": "AI Review Meeting",
        "date": "2026-05-28",
        "time": "19:00",
        "duration_hours": 1
    }}

    User Request:
    {task}
    """

    response = generate_response(prompt)

    print("Raw Calendar Agent Response:")
    print(response)

    try:

        json_match = re.search(
            r'\{.*\}',
            response,
            re.DOTALL
        )

        if json_match:

            clean_json = json_match.group()

            return json.loads(clean_json)

    except Exception as e:

        print("Calendar parsing failed:", e)

    return None