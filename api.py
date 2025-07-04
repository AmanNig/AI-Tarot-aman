from fastapi import FastAPI
from pydantic import BaseModel
import datetime
from langdetect import detect
from deep_translator import GoogleTranslator
from utils.intent import classify_intent
from core.tarot_reader import perform_reading
from initialize.cache import get_cached, set_cached
from utils.context import create_context
from typing import Optional

app = FastAPI()

class AskRequest(BaseModel):
    question: str
    language: str = 'en'

class AskResponse(BaseModel):
    detected_language: str
    intent: str
    result_text: str
    result: dict
    translated_question: str
    translated_result: Optional[str] = None
    timing: Optional[dict] = None


def format_date(dt: datetime.date) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

def detect_and_translate(input_text: str, target_language='en'):
    detected_language = detect(input_text)
    if detected_language != target_language:
        translator = GoogleTranslator(source='auto', target=target_language)
        return translator.translate(input_text), detected_language
    return input_text, detected_language

def translate_back(result_text: str, target_language: str):
    if target_language == 'en':
        return result_text
    translator = GoogleTranslator(source='en', target=target_language)
    return translator.translate(result_text)

@app.post("/ask", response_model=AskResponse)
async def ask_question(payload: AskRequest):
    import time
    question = payload.question.strip()
    lang = payload.language.strip().lower() if payload.language else 'en'
    context = create_context(language=lang)
    timing = {}

    # 1️⃣ Detect & translate
    t0 = time.time()
    translated_q, detected_lang = detect_and_translate(question, target_language='en')
    timing['lang_detect_translate'] = time.time() - t0

    # 2️⃣ Try cache
    cached = get_cached(question)
    if cached:
        result = cached
        intent = result.get("intent", "general")
        from_cache = True
    else:
        from_cache = False
        t_start = time.time()
        # 3️⃣ Intent
        t0 = time.time()
        intent = classify_intent(translated_q)
        timing['intent_classification'] = time.time() - t0

        # 4️⃣ Perform
        t1 = time.time()
        result = perform_reading(translated_q, intent, context.get_history())
        timing['prediction'] = time.time() - t1
        timing['total'] = time.time() - t_start

        if "error" in result:
            return AskResponse(
                detected_language=detected_lang,
                intent=intent,
                result_text=f"Error: {result['error']}",
                result=result,
                translated_question=translated_q,
                timing=timing
            )

        # 5️⃣ Store intent & dates
        result["intent"] = intent
        if dr := result.get("date_range"):
            result["date_range"] = [dr[0].isoformat(), dr[1].isoformat()]
        set_cached(question, result)

    # 6️⃣ Add turn into context
    context.add_entry(
        question=question,
        translated=translated_q,
        intent=intent,
        result=result
    )

    # 7️⃣ Build result_text
    if intent == "factual":
        result_text = "Sorry, I cannot provide factual information at the moment. Please ask a tarot-related question."
    elif intent == "conversation":
        result_text = result["interpretation"]
    elif intent == "timeline" and result.get("card"):
        card = result["card"]
        ds, de = result["date_range"]
        ds_dt = datetime.date.fromisoformat(ds)
        de_dt = datetime.date.fromisoformat(de)
        result_text = (
            f"Card: {card}\n"
            f"Timeframe: {format_date(ds_dt)} – {format_date(de_dt)}\n\n"
            f"{result['interpretation']}"
        )
    else:
        if cards := result.get("cards"):
            result_text = f"Cards Drawn: {', '.join(cards)}\n\n{result['interpretation']}"
        else:
            result_text = result["interpretation"]

    # 8️⃣ Translate back if needed
    translated_result = None
    if detected_lang != 'en':
        translated_result = translate_back(result_text, detected_lang)

    return AskResponse(
        detected_language=detected_lang,
        intent=intent,
        result_text=result_text,
        result=result,
        translated_question=translated_q,
        translated_result=translated_result,
        timing=timing if not from_cache else None
    ) 