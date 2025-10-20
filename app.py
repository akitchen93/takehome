import streamlit as st
from data_loader import load_signals, fetch_linear_issues
from analytics import feedback_summary, issue_topics, compute_alignment, add_llm_topics
from matcher import match_terms_to_issues, match_to_llm_topics
import pandas as pd
import plotly.express as px

st.title("BuildBetter Take-Home Dashboard")

with st.spinner("Loading data..."):
    signals_df = load_signals("signals.json")
    linear_df = fetch_linear_issues()

tab1, tab2, tab3 = st.tabs(["Feedback Analytics", "Linear Analytics", "Alignment"])
top_count = 10
use_llm = False

if use_llm:
    linear_df = add_llm_topics(linear_df, 50)

with tab1:
    neg, pos = feedback_summary(signals_df, top_count)
    st.subheader("Top Negative Topics")
    st.dataframe(neg)
    st.subheader("Top Positive Topics")
    st.dataframe(pos)

with tab2:
    st.subheader("Engineering")
    st.write("Top in progress")
    st.dataframe(issue_topics(linear_df, "started", "Engineering", top_count, use_llm))
    st.write("Top completed")
    st.dataframe(issue_topics(linear_df, "completed", "Engineering", top_count, use_llm))

    st.subheader("Customer Support")
    st.write("Top in progress")
    st.dataframe(issue_topics(linear_df, "started", "Customer Support", top_count, use_llm))
    st.write("Top completed")
    st.dataframe(issue_topics(linear_df, "completed", "Customer Support", top_count, use_llm))

with tab3:
    neg, pos = feedback_summary(signals_df)
    top_terms = list(neg["term"]) + list(pos["term"])
    subset = signals_df[signals_df["term"].isin(top_terms)]
    
    matches = []
    if use_llm:
        matches = match_to_llm_topics(subset, linear_df)
    else:
        matches = match_terms_to_issues(subset, linear_df)
    st.subheader("Fuzzy Matches (score ≥ 80)")
    st.dataframe(matches)

    st.subheader("Alignment Summary")

    align_df = compute_alignment(signals_df, matches, linear_df)

    # main table
    st.dataframe(
        align_df[
            ["term","feedback_mentions","avg_sentiment","feedback_share",
            "total_matched_issues","issue_share","alignment_gap","Engineering","Customer Support"]
        ]
    )

    # # --- Feedback vs Issues share chart ---
    # chart_df = align_df.melt(
    #     id_vars=["term"],
    #     value_vars=["feedback_share","issue_share"],
    #     var_name="metric", value_name="share"
    # )
    # fig = px.bar(
    #     chart_df, x="term", y="share", color="metric",
    #     barmode="group", title="Feedback vs Issues Share by Topic"
    # )
    # st.plotly_chart(fig, use_container_width=True)

    # # --- Alignment gap (highlights under-served topics) ---
    # gap_fig = px.bar(
    #     align_df, x="term", y="alignment_gap",
    #     color="alignment_gap", color_continuous_scale="RdYlGn_r",
    #     title="Alignment Gap (Feedback – Issues Share)"
    # )
    # st.plotly_chart(gap_fig, use_container_width=True)