import json, time, uuid
from pathlib import Path
from app import config

LOG_PATH = Path("logs/trace_log.jsonl")
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

def estimate_tokens(text: str) -> int:
    # Rough estimate for monitoring only; use provider usage metadata when available.
    return max(1, round(len(text.split()) * 1.3)) if text.strip() else 0

def log_trace(question: str, answer: str, provider: dict, input_guardrail: dict,
              output_guardrail: dict, started_at: float, status: str = "ok") -> dict:
    latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
    record = {
        "trace_id": str(uuid.uuid4()),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "latency_ms": latency_ms,
        "input_tokens_estimated": estimate_tokens(question),
        "output_tokens_estimated": estimate_tokens(answer),
        "provider": provider,
        "input_guardrail": input_guardrail,
        "output_guardrail": output_guardrail,
        "status": status,
        "question": question[:1000],
        "answer": answer[:2000],
    }
    with LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
    _send_langfuse(record)
    return record

def _send_langfuse(record: dict):
    if not (config.LANGFUSE_PUBLIC_KEY and config.LANGFUSE_SECRET_KEY):
        return
    try:
        from langfuse import Langfuse
        client = Langfuse(
            public_key=config.LANGFUSE_PUBLIC_KEY,
            secret_key=config.LANGFUSE_SECRET_KEY,
            host=config.LANGFUSE_HOST,
        )
        trace = client.trace(
            name="llm-evaluation-demo",
            id=record["trace_id"],
            metadata={
                "latency_ms": record["latency_ms"],
                "provider": record["provider"].get("provider"),
                "status": record["status"],
            },
            input=record["question"],
            output=record["answer"],
        )
        client.flush()
    except Exception as exc:
        # Never interrupt app responses because telemetry is unavailable.
        with Path("logs/observability_errors.log").open("a", encoding="utf-8") as f:
            f.write(f"Langfuse export failed: {type(exc).__name__}: {exc}\n")
