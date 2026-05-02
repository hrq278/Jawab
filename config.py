# ============================================================
# config.py — Central config. All other files import from here.
# Keys are loaded from .env so they're never hardcoded.
# ============================================================

import os
from dotenv import load_dotenv

# Load all values from .env file into environment
load_dotenv()

# --- Gemini AI (Member 1) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- WhatsApp (Member 2) ---
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "mysecretverifytoken123")
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

# --- Google Sheets (Member 3) ---
SHEET_ID = os.getenv("SHEET_ID")
CREDENTIALS_FILE = "credentials.json"

# --- App settings ---
PORT = int(os.getenv("PORT", 8080))  # Changed from 5000 to 8080
DEBUG = os.getenv("FLASK_ENV", "development") == "development"

# --- Bot personality ---
# The AI will always reply in the same language the customer used
BOT_NAME = "Support Assistant"
ESCALATION_KEYWORDS = [
    # English
    "human", "agent", "manager", "person", "real person", "speak to someone",
    # Urdu (romanised)
    "insaan", "manager chahiye", "baat karni hai", "banda chahiye",
]
MAX_CONVERSATION_HISTORY = 5  # Remember last 5 messages per customerSHEET_ID = os.getenv("SHEET_ID")
