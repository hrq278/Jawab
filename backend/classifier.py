# ============================================================
# classifier.py — Reads a message and decides what type it is.
# Owned by Member 1.
# Returns one of: "complaint", "escalate", "query"
# ============================================================

from config import ESCALATION_KEYWORDS


# Words that suggest a complaint
COMPLAINT_KEYWORDS = [
    # English
    "complaint", "problem", "issue", "broken", "wrong", "bad", "terrible",
    "disappointed", "unhappy", "refund", "not working", "damaged", "late",
    "delay", "didn't arrive", "missing", "lost", "scam", "fraud",
    # Roman Urdu
    "shikayat", "masla", "kharab", "ghalat", "wapas", "nahi aaya",
    "der", "nuqsan", "pagal", "bura", "bekaar",
]


def classify_message(message: str) -> str:
    """
    Classify a customer message into a category.

    Args:
        message: The raw text from the customer

    Returns:
        "escalate"  — Customer wants a human agent
        "complaint" — Customer has a complaint/problem
        "query"     — General question or enquiry
    """
    message_lower = message.lower()

    # Check for escalation first — highest priority
    for keyword in ESCALATION_KEYWORDS:
        if keyword in message_lower:
            return "escalate"

    # Check for complaints
    for keyword in COMPLAINT_KEYWORDS:
        if keyword in message_lower:
            return "complaint"

    # Everything else is a general query
    return "query"


def should_escalate(message: str) -> bool:
    """Quick helper — returns True if this message needs a human agent."""
    return classify_message(message) == "escalate"