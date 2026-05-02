# ============================================================
# whatsapp_handler.py — Sends WhatsApp messages back to customer.
# Owned by Member 2. This is a STUB for now.
# M2 fills in the real implementation using Meta Cloud API.
# ============================================================

# Member 2: Replace this entire file with your real implementation.
# Use the requests library to POST to the WhatsApp Cloud API.


def send_whatsapp_message(to_phone: str, message_text: str) -> bool:
    """
    Send a WhatsApp text message to a phone number.

    Args:
        to_phone: Customer's phone number with country code e.g. "923001234567"
        message_text: The reply text to send

    Returns:
        True if sent successfully, False if failed
    """
    # STUB — prints to console until M2 implements
    print(f"[WhatsApp STUB] Sending to {to_phone}: {message_text[:80]}")
    return True


def extract_message_from_webhook(payload: dict) -> tuple:
    """
    Pull the phone number and message text out of the raw Meta webhook payload.

    Args:
        payload: The JSON dict received from Meta's webhook POST

    Returns:
        Tuple of (phone_number, message_text) or (None, None) if not a message
    """
    # STUB — M2 replaces this with real Meta payload parsing
    try:
        entry = payload["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]
        message = value["messages"][0]
        phone = message["from"]
        text = message["text"]["body"]
        return phone, text
    except (KeyError, IndexError):
        return None, None