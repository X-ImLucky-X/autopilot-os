import json
import re

from ollama_client import generate_response


def classify_task(task: str):

    prompt = f"""
    Analyze the user request and return ONLY valid JSON.

    Available tools:
    - research
    - email
    - calendar

    Rules:
    - DO NOT invent recipients
    - Only extract recipient if explicitly mentioned
    - If no email exists, recipient must be ""
    - Return ONLY JSON
    - No markdown
    - No explanations

    Example 1:

    {{
        "research": true,
        "email": true,
        "calendar": false,
        "recipient": "john@gmail.com"
    }}

    Example 2:

    {{
        "research": false,
        "email": false,
        "calendar": true,
        "recipient": ""
    }}

    Example 3:

    {{
        "research": true,
        "email": true,
        "calendar": true,
        "recipient": "john@gmail.com"
    }}

    User Request:
    {task}
    """

    response = generate_response(prompt)

    print("Raw Router Response:")
    print(response)

    try:

        json_match = re.search(
            r'\{.*\}',
            response,
            re.DOTALL
        )

        if json_match:

            clean_json = json_match.group()

            parsed = json.loads(clean_json)

            # Safety validation
            recipient = str(
                parsed.get(
                    "recipient",
                    ""
                )
            )

            if "@" not in recipient:

                parsed["recipient"] = ""

            # Ensure keys exist
            parsed.setdefault(
                "research",
                False
            )

            parsed.setdefault(
                "email",
                False
            )

            parsed.setdefault(
                "calendar",
                False
            )

            parsed.setdefault(
                "recipient",
                ""
            )

            return parsed

    except Exception as e:

        print(
            "Router parsing failed:",
            e
        )

    return {

        "research": True,

        "email": False,

        "calendar": False,

        "recipient": ""
    }