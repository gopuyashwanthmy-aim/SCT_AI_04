import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.guardrails import check_input, check_output
from app.llm import generate_answer
from app.observability import log_trace

app = FastAPI(title="LLM Evaluation, Guardrails & Observability", version="1.0.0")

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=12000)
    context: str = Field(default="", max_length=20000)

@app.get("/")
def root():
    return {"message": "LLM evaluation and safety monitoring API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(request: QueryRequest):
    started = time.perf_counter()
    input_check = check_input(request.question)
    if not input_check.allowed:
        log_trace(request.question, "", {"provider": "none"}, input_check.to_dict(),
                  {"allowed": True, "reasons": [], "category": "not_run"}, started, "blocked_input")
        raise HTTPException(status_code=400, detail={"message": "Input blocked by guardrails", "reasons": input_check.reasons})
    try:
        answer, provider = generate_answer(request.question, request.context)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM provider error: {type(exc).__name__}: {exc}")
    output_check = check_output(answer)
    if not output_check.allowed:
        answer = "[Output blocked by safety guardrails.]"
    trace = log_trace(request.question, answer, provider, input_check.to_dict(),
                      output_check.to_dict(), started, "ok" if output_check.allowed else "blocked_output")
    return {"answer": answer, "provider": provider, "guardrails": {
        "input": input_check.to_dict(), "output": output_check.to_dict()
    }, "observability": {"trace_id": trace["trace_id"], "latency_ms": trace["latency_ms"],
                         "input_tokens_estimated": trace["input_tokens_estimated"],
                         "output_tokens_estimated": trace["output_tokens_estimated"]}}
