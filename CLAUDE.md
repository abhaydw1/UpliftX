# UpliftX — Project Brief for Claude

## What this project is
UpliftX is an uplift-modeling (causal ML) retention targeting system. It answers:
**"Which customers will be retained BECAUSE of an offer?"**, not just "who will churn?".
It ranks customers by the causal effect of an offer, groups them into 4 segments,
decides who to target under a fixed budget using expected value, explains the drivers
with SHAP, drafts personalised offers with an LLM, and exports data for a Power BI dashboard.

Purpose: portfolio project for an analytics consulting role (EXL Decision Analytics).
Business framing and clear explanations matter as much as model performance.

## How to work with me (IMPORTANT)
- I am learning while building. Work **one step at a time** (see Build Steps below).
- For each step: explain WHAT and WHY in 3–4 lines, then give the code with clear comments.
- Do not write the whole project in one go. Wait for me to run each step and share output.
- Keep code simple and readable over clever. Prefer plain pandas/sklearn where possible.
- After each step, tell me 2–3 things I should be able to explain in an interview.

## Core concepts
- **Uplift** = P(outcome | treatment) − P(outcome | control) for a customer.
- **Segments** (from predicted p_T and p_C):
  - Persuadables: high p_T, low p_C → TARGET
  - Sure Things: high p_T, high p_C → don't target (wasted offer)
  - Lost Causes: low p_T, low p_C → don't target
  - Sleeping Dogs: p_T < p_C → NEVER target (offer hurts)
- **T-learner**: separate models on treated and control; uplift = difference of predictions.
- **X-learner**: two-stage meta-learner that imputes individual effects; better with unbalanced groups.
- Individual uplift is never observed, so evaluation uses **Qini curve / Qini AUC, uplift curve (AUUC),
  uplift@k, and a decile table** — not accuracy.

## Dataset
- **Hillstrom E-Mail Marketing dataset** (MineThatData), loaded via
  `from sklift.datasets import fetch_hillstrom`.
- ~64,000 customers who purchased in the last 12 months, randomly assigned to:
  Mens E-Mail / Womens E-Mail / No E-Mail. Outcomes tracked for 2 weeks.
- Features: recency, history (past-year spend), mens, womens, zip_code, newbie, channel.
- Targets: visit, conversion, spend.

### Modeling decisions (state these in README as assumptions)
- **Treatment** = received any email (treatment=1) vs No E-Mail (treatment=0).
  (Alternative to compare later: Womens E-Mail vs No E-Mail.)
- **Retention outcome** = `visit` within 2 weeks (re-engagement proxy for retention).
- **Customer value** = `history`.
- Offer cost assumption: configurable constant (default ₹20 per contact) in `src/config.py`.

## Tech stack
Python 3.11, pandas, numpy, scikit-learn, xgboost, scikit-uplift (sklift), causalml
(if causalml fails to install, implement T- and X-learner manually with XGBoost),
shap, matplotlib, SQLite (sqlite3), python-dotenv, LLM via Groq or Gemini free API,
Power BI (dashboard built manually from exported CSVs). Editor: VS Code.

## Folder structure
```
UpliftX/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .env                    # LLM API key (never commit)
├── .gitignore              # venv/, .env, data/*.db, __pycache__/
├── data/                   # uplift.db (SQLite), exported CSVs
├── sql/analysis.sql
├── src/
│   ├── config.py           # paths, constants (offer cost, random seed, k values)
│   ├── load_data.py        # fetch Hillstrom -> clean -> save to SQLite
│   ├── run_sql.py          # runs sql/analysis.sql, prints results
│   ├── features.py         # encoding + stratified split (on treatment+outcome)
│   ├── models.py           # T-learner, X-learner
│   ├── evaluate.py         # qini AUC, uplift@k, decile table, qini plot
│   ├── decision.py         # 4 segments, EV, budget strategy comparison
│   ├── explain.py          # surrogate model + SHAP
│   ├── offer_agent.py      # LLM drafts offers for Persuadables (JSON output)
│   └── export.py           # CSVs for Power BI
├── notebooks/              # optional exploration
└── reports/figures/        # saved plots
```

## Build steps (do in order, one per session)
0. Environment: venv, requirements.txt, .gitignore.
1. `load_data.py`: fetch data, create `treatment` and `target` columns, save table `customers` to SQLite.
2. `sql/analysis.sql` + `run_sql.py`: 5–6 queries —
   group sizes; randomization/balance check (avg recency, history, newbie share per group);
   visit & conversion rate per group; overall uplift; uplift by channel / newbie / recency band
   (CASE WHEN); a CTE + window function ranking segments by uplift.
3. `features.py`: one-hot encode zip_code & channel; stratified train/test split (70/30) on
   treatment+target combined; fixed random seed.
4. `models.py`: T-learner and X-learner with XGBoost classifiers; return uplift, p_T, p_C.
5. `evaluate.py`: Qini AUC, uplift AUC, uplift@10/20/30%, decile table (actual treated − control
   visit rate per predicted-uplift decile), Qini curve plot. Compare vs random baseline.
   Pick the best model and print a summary — these numbers go on the resume.
6. `decision.py`: assign 4 segments; EV = uplift × value × conversion_factor − offer_cost;
   compare strategies: target none / all / random 20% / model top 20% by EV → net value table;
   sensitivity to offer cost (×1, ×2).
7. `explain.py`: train XGBoost regressor on predicted uplift (surrogate), SHAP summary plot +
   2–3 individual explanations; print top drivers of being a Persuadable.
8. `offer_agent.py`: for Persuadables, send segment + top 3 SHAP drivers + value to LLM;
   force JSON {message, offer_type, max_discount}; cap discount in prompt; save to CSV.
   Read API key from .env.
9. `export.py`: CSVs for Power BI — experiment summary, decile table, segment counts,
   strategy comparison, customer-level scores (id, segment, uplift, EV, action).
   Then give step-by-step Power BI instructions (2 pages: Experiment Overview, Targeting & Budget).
10. README: problem → data → approach → results (real numbers) → recommendation → limitations
    (one campaign, 2-week window, visit as proxy, value = past spend).

## Resume claims this project must support (all must be truly implemented)
- Uplift modeling with T-/X-learner to find customers whose behaviour changes with an offer.
- Expected-value framework allocating a fixed budget across the 4 segments.
- SQL pipelines for segment analysis; SHAP churn-driver explanations; LLM agent drafting
  personalised offers; Power BI dashboard.

## Conventions
- Fixed random seed (42) everywhere; constants live in `config.py`.
- Every script runnable as `python -m src.<module>` from repo root.
- Print clear, labelled outputs; save plots to `reports/figures/`.
- Never commit `.env`, `venv/`, or the `.db` file.
- Small, frequent git commits with clear messages.
