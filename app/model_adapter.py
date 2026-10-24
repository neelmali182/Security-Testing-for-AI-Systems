"""A deterministic local stand-in for an AI model; no external model is called."""

MAX_TEXT_LENGTH = 2000
POSITIVE_WORDS = {"good", "great", "helpful", "excellent", "safe"}
NEGATIVE_WORDS = {"bad", "harmful", "awful", "unsafe", "terrible"}
INJECTION_TERMS = ("ignore all previous", "ignore your instructions", "disregard your rules", "developer mode")
UNSAFE_TERMS = (
    "build a weapon",
    "steal someone's password",
    "steal a password",
    "kill someone",
    "murder someone",
    "poison someone",
    "hurt someone",
    "harm someone",
    "make a bomb",
    "attack someone",
)
CREDENTIAL_REQUEST_TERMS = (
    "login details",
    "login credentials",
    "bank users",
    "bank customers",
    "user credentials",
    "user passwords",
    "passwords",
    "credit card information",
    "bank account details",
    "bank account information",
    "account details",
    "account information",
    "bank details",
    "account number",
    "account numbers",
    "routing number",
    "iban",
    "swift code",
    "access tokens",
    "api keys",
)


def validate_text(text: object) -> str:
    if not isinstance(text, str):
        raise TypeError("Input must be a string")
    normalized = text.strip()
    if not normalized:
        raise ValueError("Input must not be blank")
    if len(normalized) > MAX_TEXT_LENGTH:
        raise ValueError(f"Input must be at most {MAX_TEXT_LENGTH} characters")
    return normalized


def classify(text: object) -> dict:
    """Return deterministic sentiment-like labels for a small demo vocabulary."""
    normalized = validate_text(text)
    words = set(normalized.lower().split())
    positive = len(words & POSITIVE_WORDS)
    negative = len(words & NEGATIVE_WORDS)
    label = "positive" if positive > negative else "negative" if negative > positive else "neutral"
    confidence = 0.75 if positive != negative else 0.5
    return {"label": label, "confidence": confidence}


def answer_prompt(text: object, protected_value: str | None = None) -> dict:
    """Return a policy-checked canned response for security test demonstrations."""
    normalized = validate_text(text)
    lowered = normalized.lower()
    blocked = any(term in lowered for term in INJECTION_TERMS + UNSAFE_TERMS + CREDENTIAL_REQUEST_TERMS)
    if blocked:
        response = "I cannot help with that request."
    elif "secret" in lowered or "token" in lowered or "hidden" in lowered:
        response = "I cannot disclose protected information."
    else:
        response = "This is a local demonstration response."
    if protected_value and protected_value in normalized and protected_value not in response:
        response = "I cannot disclose protected information."
    return {"response": response, "blocked": blocked or response.startswith("I cannot disclose")}
