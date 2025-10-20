"""
Fuzzy matching between feedback terms and Linear issues.
"""

from rapidfuzz import fuzz
import pandas as pd


def match_score(text, term):
    text = (text or "").lower()
    term = term.lower()
    if term in text:
        return 100
    return fuzz.partial_ratio(text, term)


def match_terms_to_issues(signals_df: pd.DataFrame, linear_df: pd.DataFrame, min_score=80):
    matches = []
    for term in signals_df["term"].unique():
        for _, issue in linear_df.iterrows():
            project_name = issue.get("project.name") if "project.name" in issue and pd.notna(issue.get("project.name")) else ""
            text = " ".join(filter(None, [
                issue.get("title", ""),
                project_name,
                issue.get("description", "")
            ])).lower()
            score = match_score(text, term)
            if score >= min_score:
                matches.append({
                    "term": term,
                    "issue": issue.get("title"),
                    "team": issue.get("team.name"),
                    "score": score
                })
    return pd.DataFrame(matches)

def match_to_llm_topics(signals_df, linear_df, min_score=80):
    matches = []
    for term in signals_df["term"].unique():
        for _, issue in linear_df.iterrows():
            topics = issue.get("llm_topics") or []
            best = max((fuzz.ratio(term, t) for t in topics), default=0)
            if best >= min_score:
                matches.append({
                    "term": term,
                    "issue": issue["title"],
                    "team": issue.get("team.name"),
                    "score": best
                })
    return pd.DataFrame(matches)