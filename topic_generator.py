from openai import OpenAI
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_issue_topics(title, description):
    text = f"Title: {title}\nDescription: {description}"
    prompt = f"""
    You are helping categorize product development issues.

    Given this text, extract 3 to 5 short product or feature topics 
    that summarize what this issue is about. 
    Return them as a valid JSON array of lowercase strings.
    If there is not enough information, return an empty array.

    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    # parse model output safely
    raw = response.choices[0].message.content.strip()
    try:
        topics = json.loads(raw)
        if isinstance(topics, list):
            return [t.lower() for t in topics]
    except Exception:
        # fallback: split by comma if not valid JSON
        return [t.strip().lower() for t in raw.split(",") if t]
    return []

