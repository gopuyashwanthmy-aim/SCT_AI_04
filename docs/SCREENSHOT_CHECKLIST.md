# Screenshot and Log Evidence Checklist

Capture genuine screenshots after running the project locally:
1. `01_installation_and_demo.png` — terminal showing dependencies installed and `python -m app.demo` success.
2. `02_evaluation_report.png` — open `reports/evaluation_report.md` showing the benchmark table.
3. `03_safety_report.png` — open `reports/safety_report.md` showing PASS/FAIL tests.
4. `04_api_docs.png` — browser at `http://127.0.0.1:8000/docs`.
5. `05_api_success.png` — successful POST `/ask` with response, guardrail result and latency.
6. `06_api_blocked.png` — POST `/ask` with prompt-injection text returning HTTP 400.
7. `07_trace_logs.png` — terminal or editor showing `logs/trace_log.jsonl` entries.
8. Optional `08_langfuse_dashboard.png` — actual trace visible in your Langfuse project after valid credentials are configured.

Do not fabricate screenshots. Capture them from your own run. Do not show `.env` or any API key in screenshots.
