import requests


OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL = "qwen2.5:7b"


def generate_response(prompt: str):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()

    return data["response"]