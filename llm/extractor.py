import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

MODEL = "llama-3.3-70b-versatile"


def extract_internship_data(raw_text):

    prompt = f"""
You are an AI internship extraction assistant.

Extract internship details from the text below.

Return ONLY valid JSON.

Required format:

[
  {{
    "Company": "",
    "Role": "",
    "Location": "",
    "Internship URL": "",
    "Skills": [],
    "Posted Date": ""
  }}
]

Text:
{raw_text}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0
    }

    try:

        response = requests.post(
            GROQ_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        response.raise_for_status()

        result = response.json()["choices"][0]["message"]["content"]

        # Remove markdown if model adds it
        result = result.replace("```json", "")
        result = result.replace("```", "")
        result = result.strip()

        parsed = json.loads(result)

        if isinstance(parsed, list):
            return parsed

        return []

    except Exception as e:
        print(f"Groq Extraction Error: {e}")
        return []