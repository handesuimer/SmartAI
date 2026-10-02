import requests

from config import Config

import markdown

def ask_ai(message):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {
                "role": "system",
                "content": Config.BUSINESS_CONTEXT,
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        "temperature": 0.7,
    }

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=30,
    )

    response.raise_for_status()

    result = response.json()

    return markdown.markdown(
    result["choices"][0]["message"]["content"]
)