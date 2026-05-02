# ============================================================
# app.py — The main Flask server. Central hub of the entire bot.
# ============================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, render_template
from config import VERIFY_TOKEN, DEBUG, PORT
from ai_engine import get_ai_reply
from classifier import classify_message
from sheets_handler import log_ticket, get_conversation_history, save_message, get_all_tickets
from whatsapp_handler import send_whatsapp_message, extract_message_from_webhook

# Tell Flask to look in frontend folder for templates and static files
app = Flask(__name__, 
            template_folder='../frontend/templates',
            static_folder='../frontend/static')

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({
        "status": "running",
        "message": "AI Support Bot is online",
        "version": "1.0"
    }), 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("[Webhook] Meta verification successful")
        return challenge, 200
    else:
        print("[Webhook] Verification failed — token mismatch")
        return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def receive_whatsapp_message():
    payload = request.get_json()
    if not payload:
        return "Bad Request", 400
    phone, message_text = extract_message_from_webhook(payload)
    if not phone or not message_text:
        return "OK", 200
    category = classify_message(message_text)
    is_escalated = (category == "escalate")
    history = get_conversation_history(phone)
    ai_reply = get_ai_reply(message_text, history)
    log_ticket(phone, message_text, category, is_escalated)
    save_message(phone, "user", message_text)
    save_message(phone, "model", ai_reply)
    send_whatsapp_message(phone, ai_reply)
    return "OK", 200

@app.route("/chat", methods=["POST"])
def web_chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "No message provided"}), 400
    message_text = data["message"].strip()
    session_id = data.get("session_id", "web-user")
    category = classify_message(message_text)
    is_escalated = (category == "escalate")
    history = get_conversation_history(session_id)
    ai_reply = get_ai_reply(message_text, history)
    log_ticket(session_id, message_text, category, is_escalated)
    save_message(session_id, "user", message_text)
    save_message(session_id, "model", ai_reply)
    return jsonify({
        "reply": ai_reply,
        "category": category,
        "escalated": is_escalated
    }), 200

@app.route("/tickets", methods=["GET"])
def get_tickets():
    tickets = get_all_tickets()
    return jsonify({"tickets": tickets, "count": len(tickets)}), 200

@app.route("/chat-page", methods=["GET"])
def chat_page():
    return render_template("index.html")

@app.route("/dashboard", methods=["GET"])
def dashboard_page():
    return render_template("dashboard.html")

if __name__ == "__main__":
    print("=" * 50)
    print(" AI Support Bot — Starting up")
    print(f" Running on http://localhost:{PORT}")
    print(f" Debug mode: {DEBUG}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
