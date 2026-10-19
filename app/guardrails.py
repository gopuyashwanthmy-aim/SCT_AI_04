import re
from dataclasses import dataclass, asdict

INJECTION_PATTERNS = [
    r"ignore (all )?(previous|prior) instructions",
    r"reveal (the )?(system prompt|hidden prompt|secrets?)",
    r"developer message",
    r"bypass (the )?(safety|guardrails|rules)",
    r"jailbreak",
    r"act as an unrestricted",
]
TOXIC_PATTERNS = [
    r"\bkill yourself\b",
    r"\bi will hurt you\b",
    r"\b(?:racial slur placeholder)\b",
]

@dataclass
class GuardrailResult:
    allowed: bool
    reasons: list[str]
    category: str = "safe"

    def to_dict(self):
        return asdict(self)

def check_input(text: str) -> GuardrailResult:
    reasons = []
    normalized = (text or "").lower()
    if not normalized.strip():
        reasons.append("empty_input")
    if len(text or "") > 12000:
        reasons.append("input_too_long")
    if any(re.search(p, normalized, re.IGNORECASE) for p in INJECTION_PATTERNS):
        reasons.append("possible_prompt_injection")
    if any(re.search(p, normalized, re.IGNORECASE) for p in TOXIC_PATTERNS):
        reasons.append("potentially_toxic_language")
    return GuardrailResult(not reasons, reasons, "blocked" if reasons else "safe")

def check_output(text: str) -> GuardrailResult:
    reasons = []
    if not (text or "").strip():
        reasons.append("empty_output")
    if re.search(r"(api[_ -]?key|password)\s*[:=]\s*\S+", text or "", re.IGNORECASE):
        reasons.append("possible_secret_disclosure")
    return GuardrailResult(not reasons, reasons, "blocked" if reasons else "safe")
