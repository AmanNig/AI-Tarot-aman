import streamlit as st
import datetime
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from langdetect import detect
from deep_translator import GoogleTranslator
from utils.intent import classify_intent
from core.tarot_reader import perform_reading
from initialize.cache import get_cached, set_cached
from utils.context import create_context

st.set_page_config(page_title="TarotTara - Your Magical Guide", layout="centered")
st.title("🔮 TarotTara – Your Magical Tarot Guide")

# Session state for storing user info and context
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "language" not in st.session_state:
    st.session_state.language = "en"
if "context" not in st.session_state:
    st.session_state.context = create_context(language=st.session_state.language)
if "farewell" not in st.session_state:
    st.session_state.farewell = False

# Sidebar: User Info
with st.sidebar:
    st.header("📋 User Info")
    with st.form("user_form"):
        name = st.text_input("Full Name")
        dob = st.text_input("Date of Birth (DD-MM-YYYY)")
        birth_place = st.text_input("Place of Birth")
        birth_time = st.text_input("Time of Birth (e.g. 03:30 PM)")
        gender = st.selectbox("Gender", ["M", "F", "Other"])
        mood = st.text_input("How are you feeling today?")
        day_summary = st.text_input("How is your day going?")
        language = st.selectbox("Preferred Language", ["en", "hi", "es", "fr"], index=0)
        submit = st.form_submit_button("Save Info")

    if submit:
        user_info = {
            "name": name,
            "dob": dob,
            "birth_place": birth_place,
            "birth_time": birth_time,
            "gender": gender,
            "mood": mood,
            "day_summary": day_summary,
        }
        st.session_state.user_info = user_info
        st.session_state.language = language
        st.session_state.context = create_context(language=language)
        st.success("User info saved successfully!")

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

# Main app input section
st.subheader("🧘 Ask your question (type 'exit' to quit)")
input_method = st.radio("Choose input method", ["Type"], horizontal=True)

question = ""
if not st.session_state.farewell:
    if input_method == "Type":
        question = st.text_area("Type your question below:")

    if st.button("🔮 Submit Question") and question.strip():
        if question.strip().lower() == "exit":
            st.session_state.farewell = True
            st.success("🌙 Farewell. Trust the journey ahead. 👋 Goodbye!")
        else:
            with st.spinner("Analyzing your question..."):
                detected_lang = detect(question)
                translated_question, detected_lang = detect_and_translate(question, target_language='en')

                t0 = time.time()
                intent = classify_intent(translated_question)
                intent_duration = time.time() - t0

                cached = get_cached(question)
                if cached:
                    st.info("🧠 Serving from Redis cache!")
                    result = cached
                else:
                    t1 = time.time()
                    result = perform_reading(translated_question, intent, st.session_state.context.get_history())
                    prediction_duration = time.time() - t1
                    result["intent"] = intent
                    if dr := result.get("date_range"):
                        result["date_range"] = [dr[0].isoformat(), dr[1].isoformat()]
                    set_cached(question, result)
                st.session_state.context.add_entry(
                    question=question,
                    translated=translated_question,
                    intent=intent,
                    result=result
                )

                # Build result_text
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

                # Display
                st.markdown("### 🔍 TarotTara says:")
                st.write(result_text)

                # Translate back if needed
                user_lang = st.session_state.language
                if detected_lang != 'en':
                    back = translate_back(result_text, detected_lang)
                    st.write(f"**Result in {detected_lang}:**\n{back}")
                elif user_lang != 'en':
                    back = translate_back(result_text, user_lang)
                    st.write(f"**Result in {user_lang}:**\n{back}")

                st.markdown(f"⏱️ **Intent classification:** {intent_duration:.2f}s")
                if not cached:
                    st.markdown(f"⏱️ **Prediction (LLM + RAG):** {prediction_duration:.2f}s")
else:
    st.success("🌙 Farewell. Trust the journey ahead. 👋 Goodbye!") 