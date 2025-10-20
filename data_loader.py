"""
Loads customer signals and Linear issues.
"""

import json
import os
import pandas as pd
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()  # reads .env file automatically

LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")

def load_signals(path: str = "signals.json") -> pd.DataFrame:
    """Explode each signal → one row per topic/keyword with sentiment & metadata."""
    rows = []
    with open(path) as f:
        data = json.load(f)

    for s in data:
        sentiment = s.get("sentiment", 0)
        topics = [t["name"] for t in s.get("topics", []) if t.get("name")]
        keywords = [k["name"] for k in s.get("keywords", []) if k.get("name")]
        for term in set(topics + keywords):
            rows.append({
                "signal_id": s.get("id"),
                "term": term.lower(),
                "sentiment": sentiment,
                "summary": s.get("summary"),
                "exactQuote": s.get("exactQuote"),
                "types": [t["name"] for t in s.get("types", []) if t.get("name")],
                "impacts": [i["name"] for i in s.get("impacts", []) if i.get("name")],
                "company": s.get("person", {}).get("company"),
                "date": s.get("date")
            })
    return pd.DataFrame(rows)


def fetch_linear_issues(days: int = 90) -> pd.DataFrame:
    """Pull recent Linear issues via GraphQL."""
    API_URL = "https://api.linear.app/graphql"
    after = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")


    query = """
    query Issues($after: DateTimeOrDuration!) {
      issues(filter: { createdAt: { gte: $after } }, first: 250) {
        nodes {
          id 
          identifier 
          title 
          description 
          createdAt 
          completedAt
          state { name type }
          team { name }
          project { name }
          labels { nodes { name } }
        }
      }
    }
    """

    headers = {"Authorization": LINEAR_API_KEY, "Content-Type": "application/json"}
    resp = requests.post(API_URL, json={"query": query, "variables": {"after": after}}, headers=headers)
   
    resp.raise_for_status()
    issues = resp.json()["data"]["issues"]["nodes"]

    df = pd.json_normalize(issues)
 
    df["createdAt"] = pd.to_datetime(df["createdAt"])
    df["completedAt"] = pd.to_datetime(df["completedAt"])
    return df
