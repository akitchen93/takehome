# BuildBetter Take-Home

### Goal
This prototype explores how to connect **customer feedback (qualitative signals)** with **work being done in Linear (quantitative issues)** to help answer the question:

> **“Are we building the things customers actually care about?”**

It provides a small data pipeline and dashboard that:
- Loads customer feedback signals (from `signals.json`)
- Fetches Linear issues via the Linear GraphQL API
- Automatically links them by topic/keyword similarity
- Visualizes sentiment trends, team focus, and alignment gaps


### How to Run
```bash
python3 -m pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

## Tradeoffs

I approached this project realistically, focusing on what could be accomplished within a 5-hour window.  
Fuzzy matching between Linear issues and customer feedback signals is inherently challenging. The main limitation lies in the **Linear data itself**.  

After manually reviewing several issues, most titles and descriptions were vague, technical, and lacked consistent labels.  
This makes it difficult to categorize issues in a way that aligns well with customer-facing feedback.

Rather than over-investing early in imperfect heuristics, I prioritized **building a solid foundation**: ingesting the data, wiring up analytics, and visualizing initial results.  
This scaffolding creates a clear starting point to iterate on and measure improvement as matching methods evolve.

The next phase will focus on improving how we categorize and link issues, as outlined in the *Improvements* section.


# Current Capabilities
- Data Ingestion
- Feedback Analytics: view top positive/negative sentiment topics from signals
- Breaks down Linear issues by team and state
    - allows manual review of common terms to help further optimize 
- Metrics: 
    - view fuzzy matches mostly for manual checking
    - alignment summary: most insightful, shows total mentions of terms, avg sentiment, total matched issues, etc
- Started integrations with openai to try to improve Linear topics to normalize matching
    - Note: OpenAI calls are turned off by default, can toggle boolean in app, but currently calls are too slow, need to add batching as described below


# Improvements/TODOs
- batch and cache llm topics to file
- refine llm prompt to normalize vocabulary
- additional normalization/filtering for matching
- add manual review of matches, requires storage
- add deeper insights per topic ie for bugs what are the most common topics
- Use text embeddings to compute cosine similarity between signals and issues for more robust linking beyond keyword overlap.

# AI use
- Discussed project plan with ChatGPT, created iterative plan and built scaffolding
- Used Claude CLI for code review, debugging, cleanup