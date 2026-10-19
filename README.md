# LLM Evaluation, Guardrails & Open Observability

A reproducible demo suite for evaluating an LLM app, applying input/output safety checks, and observing request traces with Langfuse.

## Features
- Evaluation with DeepEval-compatible custom metrics: answer relevance, faithfulness, and hallucination-risk proxy.
- Input/output guardrails: prompt-injection patterns, toxic-language heuristics, and basic output checks.
- OpenTelemetry-style structured JSONL logs for every request, including latency, token estimates, status, and safety decisions.
- Optional Langfuse integration using environment variables.
- Demo mode works without an API key; optional Google Gemini integration.

> **Important:** Heuristic safety checks and the included demo evaluator are educational baselines, not production-grade moderation or a substitute for human review. The hallucination metric is a simple reference-overlap proxy, not a factuality proof.

## Quick start (Windows CMD)

```bat
cd llm_eval_guardrails_observability
py -m venv .venv
.venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python -m app.demo
```

The demo runs offline with sample prompts and writes:
- `reports/evaluation_report.md`
- `reports/safety_report.md`
- `logs/trace_log.jsonl`

## Run the API

```bat
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API docs.

## Optional Gemini API

1. Add your key to `.env` as `GEMINI_API_KEY=...`.
2. Set `LLM_PROVIDER=gemini`.
3. Install dependencies and run the API. The app uses the current Google Gen AI SDK and configurable `GEMINI_MODEL` (default `gemini-3.8-flash`; change it if your account doesn't expose that model).
4. Never commit `.env` or API keys.

## Optional Langfuse

Set `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_HOST` in `.env`. The app attempts to send traces when credentials are configured; local JSONL logs are always written. Verify Langfuse SDK compatibility and project credentials in your environment.

## Evaluation design

The offline evaluator reports:
- **Answer relevance proxy**: lexical overlap between question and answer.
- **Faithfulness proxy**: overlap of answer terms with supplied context.
- **Hallucination-risk proxy**: answer terms unsupported by the reference context (not a definitive hallucination detector).

For a benchmark submission, replace or supplement these baselines with DeepEval/Ragas judge-based metrics and document the judge model, dataset, thresholds, and limitations.

## Repository structure

```text
app/
  __init__.py
  config.py
  guardrails.py
  llm.py
  evaluation.py
  observability.py
  main.py
  demo.py
reports/
  evaluation_report.md
  safety_report.md
logs/
  .gitkeep
tests/
  test_guardrails.py
  test_evaluation.py
```

## Safety and privacy
- Do not log API keys or raw secrets.
- Trace logs contain prompts and answers in this educational demo; use synthetic data only. For sensitive deployments, redact or hash user content.
