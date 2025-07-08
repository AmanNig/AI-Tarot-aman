import streamlit as st
import datetime
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.language_detector import detect_and_translate, translate_back, language_detector
from utils.intent import classify_intent
from core.tarot_reader import perform_reading
from initialize.cache import get_cached, set_cached
from utils.context import create_context
from utils.api_storage import store_tarot_response, generate_session_number, calculate_duration

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
if "session_start_time" not in st.session_state:
    st.session_state.session_start_time = time.time()
if "session_number" not in st.session_state:
    st.session_state.session_number = generate_session_number()
if "user_registered" not in st.session_state:
    st.session_state.user_registered = False

# Sidebar: User Info
with st.sidebar:
    st.header("📋 User Info")
    with st.form("user_form"):
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        dob = st.text_input("Date of Birth (DD-MM-YYYY) *", placeholder="e.g. 15-03-1990")
        birth_place = st.text_input("Place of Birth *", placeholder="e.g. Mumbai, India")
        birth_time = st.text_input("Time of Birth (e.g. 03:30 PM) *", placeholder="e.g. 03:30 PM")
        gender = st.selectbox("Gender *", ["", "M", "F", "Other"])
        mood = st.text_input("How are you feeling today?", placeholder="e.g. Happy, Anxious, Excited")
        day_summary = st.text_input("How is your day going?", placeholder="Brief description of your day")
        
        # Get Indian languages
        from utils.language_detector import get_indian_languages
        indian_langs = get_indian_languages()
        
        # Create language options
        language_options = {
            "en": "English",
            **indian_langs,  # Add all Indian languages
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "it": "Italian",
            "pt": "Portuguese"
        }
        
        language = st.selectbox("Preferred Language *", list(language_options.keys()), index=0, format_func=lambda x: language_options[x])
        
        # Add note about Romanized Hindi
        if language == "hi_rom":
            st.info("💡 **Romanized Hindi**: Use this for Hindi written in English letters (e.g., 'mai aj kya kru?', 'kya haal hai?')")
        
        submit = st.form_submit_button("🔮 Begin My Tarot Journey")

    if submit:
        # Validate required fields
        required_fields = {
            "name": name,
            "dob": dob,
            "birth_place": birth_place,
            "birth_time": birth_time,
            "gender": gender
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value.strip()]
        
        if missing_fields:
            st.error(f"❌ Please fill in all required fields: {', '.join(missing_fields)}")
        else:
            user_info = {
                "name": name.strip(),
                "dob": dob.strip(),
                "birth_place": birth_place.strip(),
                "birth_time": birth_time.strip(),
                "gender": gender,
                "mood": mood.strip() if mood else "",
                "day_summary": day_summary.strip() if day_summary else "",
            }
            st.session_state.user_info = user_info
            st.session_state.language = language
            st.session_state.context = create_context(language=language)
            st.session_state.user_registered = True
            st.success("✨ Welcome to your tarot journey! Your information has been saved.")
    
    # Add reset functionality for registered users
    if st.session_state.user_registered:
        st.markdown("---")
        if st.button("🔄 Update My Information"):
            st.session_state.user_registered = False
            st.rerun()

def format_date(dt: datetime.date) -> str:
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"

# Language detection functions are now imported from utils.language_detector

# Check if user is registered
if not st.session_state.user_registered:
    st.markdown("""
    ## 🔮 Welcome to TarotTara - Your Magical Tarot Guide
    
    **Before we begin your mystical journey, please provide your details in the sidebar.**
    
    This information helps me provide more personalized and accurate readings for you.
    
    ---
    """)
    st.info("📋 **Please fill in your details in the sidebar to begin your tarot journey.**")
else:
    # Welcome message with user's name
    user_name = st.session_state.user_info.get("name", "Seeker")
    st.markdown(f"""
    ## 🌟 Welcome, {user_name}! 
    
    **TarotTara is ready to guide you through the mystical realms of tarot wisdom.**
    
    Ask me anything about your life, relationships, career, or any other aspect you'd like guidance on.
    
    ---
    """)
    
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
                    translated_question, detected_lang, confidence = detect_and_translate(question, target_language='en')

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
                    user_name = st.session_state.user_info.get("name", "Seeker")
                    st.markdown(f"### 🔍 TarotTara says to {user_name}:")
                    
                    # Handle transliterated languages properly
                    user_lang = st.session_state.language
                    if detected_lang != 'en':
                        translated_result = translate_back(result_text, detected_lang)
                        if detected_lang.endswith('_rom'):
                            # For transliterated languages, show the transliterated response as primary
                            st.write(translated_result)
                            with st.expander("Original English"):
                                st.write(result_text)
                        else:
                            # For native script languages, show English first, then translated
                            st.write(result_text)
                            st.write(f"**Result in {detected_lang}:**\n{translated_result}")
                    elif user_lang != 'en':
                        translated_result = translate_back(result_text, user_lang)
                        if user_lang.endswith('_rom'):
                            # For transliterated languages, show the transliterated response as primary
                            st.write(translated_result)
                            with st.expander("Original English"):
                                st.write(result_text)
                        else:
                            # For native script languages, show English first, then translated
                            st.write(result_text)
                            st.write(f"**Result in {user_lang}:**\n{translated_result}")
                    else:
                        st.write(result_text)

                    # Store response in API
                    try:
                        duration = calculate_duration(st.session_state.session_start_time)
                        api_success = store_tarot_response(
                            session_number=st.session_state.session_number,
                            time_duration=duration,
                            intent_type=intent,
                            question=question,
                            answer=result_text,
                            user_info=st.session_state.user_info
                        )
                        
                        if api_success:
                            st.success("📊 Response stored successfully!")
                        else:
                            st.warning("⚠️ Response storage failed, but reading completed successfully.")
                    except Exception as e:
                        st.warning(f"⚠️ API storage error: {str(e)}")

                    st.markdown(f"⏱️ **Intent classification:** {intent_duration:.2f}s")
                    if not cached:
                        st.markdown(f"⏱️ **Prediction (LLM + RAG):** {prediction_duration:.2f}s")
    else:
        st.success("🌙 Farewell. Trust the journey ahead. 👋 Goodbye!") 