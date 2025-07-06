# core/tarot_reader.py

import random
import datetime
# from langchain_ollama import ChatOllama
# from langchain_groq import ChatGroq
import requests
from os import getenv
from initialize.config import MODEL_NAME
from utils.deck import FULL_DECK, NUMERIC_CARDS, DATE_RANGES
from core.rag import get_card_meaning
from utils.factual import answer_factual
from typing import List, Dict, Any


def groq_invoke(prompt: str) -> str:
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = getenv("GROQ_API_KEY")  # Or use os.getenv("GROQ_API_KEY")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1024,
        "temperature": 0.7
    }
    response = requests.post(api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

SYSTEM_PROMPT = """You are TarotTara, a professional and empathic tarot reader.
You remember the last few messages and speak in a warm, respectful, and professional tone.
Maintain appropriate boundaries and avoid overly familiar terms like "sweetie", "cutie", "dear", or "honey".

Provide direct, clear, and actionable interpretations based on the cards drawn. Be specific about what the cards indicate rather than being vague or non-committal. When cards suggest positive outcomes, state them clearly. When cards indicate challenges, explain them directly and offer guidance.

Structure your response clearly:
1. Explain each card's meaning in relation to the question
2. Provide a clear interpretation of what the cards suggest
3. Give specific insights and guidance based on the reading

Keep responses focused and complete, avoiding overly long explanations that don't provide clear answers."""

def _build_history_block(history: List[Dict[str, Any]]) -> str:
    """
    Convert the conversation history (list of entries with 'question' and 'result')
    into a chat-like block:
      User: <question>
      Assistant: <interpretation>
    """
    lines = []
    for entry in history:
        q = entry.get('question', '')
        interp = entry.get('result', {}).get('interpretation', '')
        # only include if both exist
        if q:
            lines.append(f"User: {q}")
        if interp:
            lines.append(f"Assistant: {interp}")
    return "\n".join(lines)

def perform_reading(
    question: str,
    intent: str,
    history: List[Dict[str, Any]]
) -> Dict[str, Any]:
    try:
        today = datetime.date.today()
        today_str = today.strftime('%B %d, %Y')

        # Serialize past turns
        hist_block = _build_history_block(history)

        # 1) Conversational questions
        if intent == "conversation":
            prompt = f"""{SYSTEM_PROMPT}

{hist_block}

User: "{question}"

Assistant:"""
            reply = groq_invoke(prompt)
            return {"interpretation": reply, "card": None, "date_range": None}

        # 2) Factual questions: polite refusal
        if intent == "factual":
            polite = (
                "Sorry, I cannot provide factual information at the moment. "
                "Please ask a tarot-related question."
            )
            return {"interpretation": polite, "card": None, "date_range": None}

        # 3) Timeline readings
        if intent == "timeline":
            card = random.choice(NUMERIC_CARDS)
            dr = DATE_RANGES[card]
            meaning = get_card_meaning(card)
            start_str = dr[0].strftime('%B %d, %Y')
            end_str   = dr[1].strftime('%B %d, %Y')

            prompt = f"""{SYSTEM_PROMPT}

{hist_block}

User: "{question}"

You drew: {card}  ({start_str} – {end_str})
Meaning: {meaning}

Assistant:"""
            reply = groq_invoke(prompt)
            return {"card": card, "date_range": dr, "interpretation": reply}

        # 4) General 3-card spread (yes_no, guidance, insight, or general)
        cards = random.sample(FULL_DECK, k=3)
        meanings = [get_card_meaning(c, k=1) for c in cards]

        prompt = f"""{SYSTEM_PROMPT}

{hist_block}

User: "{question}"

Cards drawn:
1. {cards[0]} — {meanings[0]}
2. {cards[1]} — {meanings[1]}
3. {cards[2]} — {meanings[2]}

Assistant:"""
        reply = groq_invoke(prompt)
        return {"cards": cards, "interpretation": reply}

    except Exception as e:
        return {"error": str(e)}


