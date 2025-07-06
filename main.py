import time
import datetime
from utils.language_detector import detect_and_translate, translate_back, language_detector
from utils.intent import classify_intent
from core.tarot_reader import perform_reading
from initialize.cache import get_cached, set_cached
from utils.voice_assistant import listen_for_question   # For voice input
from utils.context import create_context                # <-- new

def format_date(dt: datetime.date) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

# Language detection functions are now imported from utils.language_detector

def main():
    print("🔮 Welcome to TarotTara – your magical tarot guide!")
    
    # Show supported Indian languages
    from utils.language_detector import get_indian_languages
    indian_langs = get_indian_languages()
    
    print("\n🇮🇳 Supported Indian Languages:")
    for code, name in indian_langs.items():
        print(f"  • {code}: {name}")
    
    print("\n🌍 Other Languages: en (English), es (Spanish), fr (French), de (German), it (Italian), pt (Portuguese)")
    print("\n💡 Tip: Use 'hi_rom' for Hindi written in English letters (like 'mai aj kya kru?')")
    
    lang = input("\nPlease select your language code: ").strip().lower()

    # ←── Create your ConversationContext here ──→
    context = create_context(language=lang)

    while True:
        method = input("\nEnter input mode (voice/chat): ").strip().lower()
        if method == 'voice':
            print("🎙️ Listening for your question...")
            question = listen_for_question() or ""
        else:
            question = input("\n🧘 Ask your question:\n> ").strip()

        if not question:
            continue
        if question.lower() in {'exit', 'quit'}:
            print("🌙 Farewell. Trust the journey ahead.")
            break

        # 1️⃣ Detect & translate
        translated_q, detected_lang, confidence = detect_and_translate(question)
        print(f"\n✨ Detected language: {detected_lang} (confidence: {confidence:.2f}) (processing in English)")

        # 2️⃣ Try cache
        cached = get_cached(question)
        if cached:
            print("🧠 Serving from Redis cache!")
            result = cached
            intent = result.get("intent", "general")
        else:
            t_start = time.time()
            # 3️⃣ Intent
            t0 = time.time()
            intent = classify_intent(translated_q)
            dt_intent = time.time() - t0
            print(f"\n✨ Intent detected: {intent} (in {dt_intent:.2f}s)")

            # 4️⃣ Perform
            t1 = time.time()
            result = perform_reading(translated_q, intent, context.get_history())
            print(perform_reading(translated_q, intent, context.get_history()))
            dt_read = time.time() - t1
            total_time = time.time() - t_start

            if "error" in result:
                print(f"⚠️ Error: {result['error']}")
                continue

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

        # 8️⃣ Display
        print("\n🔍 TarotTara says:\n")
        print(result_text)

        # 9️⃣ Translate back if needed
        if detected_lang != 'en':
            back = translate_back(result_text, detected_lang)
            print(f"\nResult in {detected_lang}:\n{back}")

        # 🔟 Timing
        if not cached:
            print("\n⏱️ Timing Summary:")
            print(f" • Intent classification: {dt_intent:.2f}s")
            print(f" • Prediction (LLM + RAG): {dt_read:.2f}s")
            print(f" • Total: {total_time:.2f}s")

    print("👋 Goodbye!")

if __name__ == "__main__":
    main()
