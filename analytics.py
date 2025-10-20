"""
Compute analytics on signals and Linear issues.
"""

import pandas as pd
from collections import Counter
from topic_generator import generate_issue_topics
import re


def feedback_summary(signals_df: pd.DataFrame, top_count=5):
    """Top positive & negative terms."""
    agg = signals_df.groupby("term").agg(
        avg_sentiment=("sentiment", "mean"),
        count=("signal_id", "nunique")
    ).reset_index()

    top_neg = agg[agg.avg_sentiment < 0].nlargest(top_count, "count")
    top_pos = agg[agg.avg_sentiment > 0].nlargest(top_count, "count")
    return top_neg, top_pos


def extract_keywords(text):
    if not isinstance(text, str):
        return []
    words = re.findall(r"[A-Za-z]{4,}", text.lower())
    return [w for w in words if w not in {"this", "that", "with", "from", "when", "calls", "call", "need"}]

def add_llm_topics(linear_df, limit=50):
    """Generate topics for each issue (limit for cost/time)."""
    linear_df = linear_df.copy()
    texts = linear_df.head(limit)[["title", "description"]]
    linear_df.loc[texts.index, "llm_topics"] = texts.apply(
        lambda row: generate_issue_topics(row["title"], row["description"]),
        axis=1
    )
    return linear_df



def issue_topics(linear_df: pd.DataFrame, state_type: str, team: str, top_count=5, use_llm: bool = False):
    """Return top frequent words in titles for team/state."""
    subset = linear_df[
        (linear_df["team.name"] == team) &
        (linear_df["state.type"] == state_type)
    ]
    words = []
    if use_llm and "llm_topics" in subset.columns:
        # --- Use LLM-generated topic lists ---
        for topics in subset["llm_topics"].dropna():
            if isinstance(topics, str):
                # if stored as JSON string, parse safely
                import json
                try:
                    topics = json.loads(topics)
                except Exception:
                    topics = [t.strip() for t in topics.split(",") if t.strip()]
            if isinstance(topics, list):
                words += [t.lower().strip() for t in topics]
    else:
        # --- Fallback to extracted keywords from title ---
        for t in subset["title"].dropna():
            words += extract_keywords(t)

    # Count frequency and return DataFrame
    top = Counter(words).most_common(top_count)
    return pd.DataFrame(top, columns=["term", "count"])


def compute_alignment(signals_df, matches_df, linear_df, min_score=80):
    """Aggregate matches into per-term alignment metrics."""
    # --- Prep feedback metrics ---
    feedback_counts = (
        signals_df.groupby("term")
        .agg(
            feedback_mentions=("signal_id", "nunique"),
            avg_sentiment=("sentiment", "mean")
        )
        .reset_index()
    )
    feedback_counts["feedback_share"] = (
        feedback_counts["feedback_mentions"] /
        feedback_counts["feedback_mentions"].sum()
    )

    # --- Prep issue metrics ---
    total_issues = len(linear_df)
    matches = matches_df[matches_df["score"] >= min_score]
    issue_matches = (
        matches.groupby(["term", "team"])
        .agg(matched_issues=("issue", "nunique"))
        .reset_index()
    )

    # total matches per term
    issue_totals = (
        issue_matches.groupby("term")["matched_issues"].sum()
        .reset_index()
        .rename(columns={"matched_issues": "total_matched_issues"})
    )

    # merge everything
    merged = feedback_counts.merge(issue_totals, on="term", how="left").fillna(0)
    merged["issue_share"] = merged["total_matched_issues"] / total_issues
    merged["alignment_gap"] = merged["feedback_share"] - merged["issue_share"]

    # team split
    team_pivot = (
        issue_matches.pivot_table(
            index="term", columns="team", values="matched_issues", aggfunc="sum"
        ).fillna(0)
    ).reset_index()

    df = merged.merge(team_pivot, on="term", how="left").fillna(0)
    df = df.sort_values("alignment_gap", ascending=False)
    return df
