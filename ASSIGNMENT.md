BuildBetter Take-Home (5 hours)

You'll get:
- signals.json — customer “signals” (themes + excerpts) from BuildBetter
- Linear API key — read access to a test workspace (GraphQL)

The task

Build a tiny associations pipeline that automatically links Linear issues ↔ BuildBetter signals. Use whatever gets you there fastest (embeddings, LLMs, keyword/heuristics, hybrid, etc.). Show the results in a simple UI or console output. Rough is fine; end-to-end is the win.

What I'm actually evaluating
- Velocity & judgment: Can you ship something real in ~5 hours? Do you pick sane defaults instead of spinning?
- Autonomy: Don't become your own bottleneck. Make decisions. If you'd ask for help IRL, note what you'd ask and keep moving.
- AI as leverage: Use AI a lot, but own the code. Be able to explain what it does and why.
- Clarity: Tell me what you did, what you skipped, and what you'd do next.

Minimum outcome
- Loads Linear issues + signals
- Produces automatic associations (include a score/reason if you can)
- Displays them clearly - a lightweight UI is preferable, but I'm open to other options.

Nice-to-haves (optional)
- Manual review/edit of associations
- Persistence (file/SQLite)
- Quick notes on model/feature choices and failure modes

Deliverables
- A fork of this repo with your implemented solution
- An README with:
    - how to run
    - approach (what you tried, tradeoffs)
    - what works / what doesn't
    - what you'd do next with more time
    - where/how you used AI

Guardrails (so we're aligned)
- Timebox ~5 hours. I don't need polish; I need your thinking + working prototype.
- Prototype energy > perfect plan. If you're torn, bias to shipping.
- If you rely on AI, defend the decisions it made (prompt, params, thresholds, etc.).
- Keep it simple. Any stack (TS/Python/Notebook/Web) is fine.

That's it. Have fun and ship