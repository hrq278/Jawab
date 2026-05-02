# ============================================================
# ai_engine.py — Talks to Gemini AI.
# Uses google.genai with gemini-2.5-flash.
# ============================================================

from google import genai
from google.genai import types
from config import GEMINI_API_KEY, BOT_NAME, MAX_CONVERSATION_HISTORY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are a friendly and professional customer support assistant for a Pakistani small business.
Your name is {bot_name}.

LANGUAGE RULE (most important):
- If the customer writes in Urdu or Roman Urdu, you MUST reply in Roman Urdu (Urdu written in English letters).
- If the customer writes in English, reply in English.
- Never mix languages unless the customer does.

BEHAVIOUR RULES:
- Be polite, helpful, and concise.
- For complaints: acknowledge the problem, apologize sincerely, and explain next steps.
- For questions: answer directly and clearly.
- If you cannot solve a problem, say: "I am connecting you to a human agent right away."
- Keep replies short — 2 to 4 sentences maximum.
- Do not make up information. If you don't know, say so.

BUSINESS CONTEXT:
You support customers of a Pakistani SME. Common topics include:
orders, delivery, payments, refunds, product questions, and complaints.
""".format(bot_name=BOT_NAME)


def get_ai_reply(customer_message: str, conversation_history: list = None) -> str:
    if conversation_history is None:
        conversation_history = []

    recent_history = conversation_history[-MAX_CONVERSATION_HISTORY:]

    contents = []
    for msg in recent_history:
        role = msg.get("role", "user")
        text = msg.get("parts", [""])[0]
        if role == "model":
            contents.append(types.Content(role="model", parts=[types.Part(text=text)]))
        else:
            contents.append(types.Content(role="user", parts=[types.Part(text=text)]))

    contents.append(types.Content(role="user", parts=[types.Part(text=customer_message)]))

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                max_output_tokens=300,
                temperature=0.7,
            )
        )
        return response.text.strip()

    except Exception as e:
        print(f"[AI Engine Error] {e}")
        return ("Sorry, I'm having a technical issue right now. "
                "Please try again in a moment, or reply 'human' to speak to an agent.")
