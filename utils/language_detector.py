import re
from typing import Tuple, Optional
from deep_translator import GoogleTranslator
import logging
import requests
from os import getenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def groq_invoke(prompt: str, max_tokens: int = 50, temperature: float = 0) -> str:
    """
    Invoke Groq API using the same approach as intent classification and tarot reader.
    
    Args:
        prompt: The prompt to send to the model
        max_tokens: Maximum tokens for response
        temperature: Temperature for response generation
        
    Returns:
        The model's response
    """
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = getenv("GROQ_API_KEY")
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return "en"  # Default fallback

def detect_language_with_groq(text: str) -> Tuple[str, float]:
    """
    Detect language using Groq model with confidence scoring.
    
    Args:
        text: Input text to detect language for
        
    Returns:
        Tuple of (language_code, confidence_score)
    """
    if not text or not text.strip():
        return 'en', 0.0
    
    text = text.strip()
    
    # For very short text, use pattern detection first
    if len(text) < 10:
        pattern_result = _detect_by_patterns(text)
        if pattern_result[1] > 0.7:
            return pattern_result
    
    # Use Groq for language detection
    prompt = f"""You are a language detection expert. Your job is to identify the language of the given text and respond with ONLY the ISO 639-1 language code.

Supported languages and their codes:
- English: en
- Hindi: hi
- Romanized Hindi (Hindi written in English letters): hi_rom
- Bengali: bn
- Telugu: te
- Tamil: ta
- Marathi: mr
- Gujarati: gu
- Kannada: kn
- Malayalam: ml
- Punjabi: pa
- Odia: or
- Assamese: as
- Urdu: ur
- Nepali: ne
- Spanish: es
- French: fr
- German: de
- Italian: it
- Portuguese: pt
- Vietnamese: vi
- Indonesian: id
- Malay: ms
- Filipino: tl
- Thai: th
- Myanmar: my
- Khmer: km
- Lao: lo
- Sinhala: si

Examples:
Text: "Hello, how are you?"
Language: en

Text: "नमस्ते, कैसे हो आप?"
Language: hi

Text: "mai aj kya kru?"
Language: hi_rom

Text: "Hola, ¿cómo estás?"
Language: es

Text: "Bonjour, comment allez-vous?"
Language: fr

Text: "வணக்கம், எப்படி இருக்கிறீர்கள்?"
Language: ta

Text: "নমস্কার, কেমন আছেন?"
Language: bn

Text: "నమస్కారం, ఎలా ఉన్నారు?"
Language: te

Now detect the language of this text:
Text: "{text}"
Language:"""

    try:
        detected_lang = groq_invoke(prompt, max_tokens=10, temperature=0).strip().lower()
        
        # Validate the detected language
        valid_languages = {
            'en', 'hi', 'hi_rom', 'bn', 'te', 'ta', 'mr', 'gu', 'kn', 'ml', 'pa', 'or', 'as', 'ur', 'ne',
            'es', 'fr', 'de', 'it', 'pt', 'vi', 'id', 'ms', 'tl', 'th', 'my', 'km', 'lo', 'si'
        }
        
        if detected_lang in valid_languages:
            confidence = _calculate_confidence(text, detected_lang)
            return detected_lang, confidence
        else:
            # Fallback to pattern detection
            return _detect_by_patterns(text)
            
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return _detect_by_patterns(text)

def _detect_by_patterns(text: str) -> Tuple[str, float]:
    """
    Fallback pattern-based detection for known languages.
    """
    # Indian Languages
    patterns = {
        'hi': (r'[\u0900-\u097F]', 0.9),  # Devanagari script
        'bn': (r'[\u0980-\u09FF]', 0.9),  # Bengali script
        'te': (r'[\u0C00-\u0C7F]', 0.9),  # Telugu script
        'ta': (r'[\u0B80-\u0BFF]', 0.9),  # Tamil script
        'gu': (r'[\u0A80-\u0AFF]', 0.9),  # Gujarati script
        'kn': (r'[\u0C80-\u0CFF]', 0.9),  # Kannada script
        'ml': (r'[\u0D00-\u0D7F]', 0.9),  # Malayalam script
        'pa': (r'[\u0A00-\u0A7F]', 0.9),  # Gurmukhi script
        'or': (r'[\u0B00-\u0B7F]', 0.9),  # Odia script
        'ur': (r'[\u0600-\u06FF]', 0.9),  # Arabic script
        'si': (r'[\u0D80-\u0DFF]', 0.9),  # Sinhala script
        'my': (r'[\u1000-\u109F]', 0.9),  # Myanmar script
        'th': (r'[\u0E00-\u0E7F]', 0.9),  # Thai script
        'km': (r'[\u1780-\u17FF]', 0.9),  # Khmer script
        'lo': (r'[\u0E80-\u0EFF]', 0.9),  # Lao script
    }
    
    for lang, (pattern, confidence) in patterns.items():
        if re.search(pattern, text):
            return lang, confidence
    
    # Romanized Hindi detection
    romanized_hindi_patterns = [
        r'\b(mai|main|mein|me)\b',  # I/me
        r'\b(aj|aaj)\b',  # today
        r'\b(kya|kyaa)\b',  # what
        r'\b(kru|karu|karun)\b',  # should I do
        r'\b(hu|hoon|hun)\b',  # am
        r'\b(tha|thi|the)\b',  # was/were
        r'\b(hoga|hogi|honge)\b',  # will be
        r'\b(kya|kyaa)\b',  # what
        r'\b(kaise|kaisa|kaisi)\b',  # how
        r'\b(kahan|kaha)\b',  # where
        r'\b(kab)\b',  # when
        r'\b(kyun|kyu)\b',  # why
        r'\b(acha|accha)\b',  # good
        r'\b(bura|buri)\b',  # bad
        r'\b(naam|name)\b',  # name
        r'\b(ghar|ghar)\b',  # home
        r'\b(kaam|kam)\b',  # work
        r'\b(dost|friend)\b',  # friend
        r'\b(pyar|prem)\b',  # love
        r'\b(shaadi|shadi)\b',  # marriage
        r'\b(naukri|job)\b',  # job
        r'\b(paise|paisa)\b',  # money
        r'\b(samay|time)\b',  # time
        r'\b(roz|daily)\b',  # daily
        r'\b(kal|tomorrow)\b',  # tomorrow
        r'\b(parso|day after)\b',  # day after tomorrow
    ]
    
    hindi_word_count = 0
    total_words = len(text.split())
    
    for pattern in romanized_hindi_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            hindi_word_count += 1
    
    # If more than 30% of words are Hindi, classify as Romanized Hindi
    if total_words > 0 and (hindi_word_count / total_words) > 0.3:
        confidence = min(0.8, 0.5 + (hindi_word_count / total_words) * 0.3)
        return 'hi_rom', confidence
    
    # European languages with accented characters
    if re.search(r'[áéíóúñü]', text):
        return 'es', 0.8
    elif re.search(r'[àâäéèêëïîôöùûüÿç]', text):
        return 'fr', 0.8
    elif re.search(r'[äöüß]', text):
        return 'de', 0.8
    
    # Default to English
    return 'en', 0.5

def _calculate_confidence(text: str, detected_lang: str) -> float:
    """
    Calculate confidence score for detected language.
    """
    # Base confidence
    confidence = 0.6
    
    # Adjust based on text length
    if len(text) > 50:
        confidence += 0.2
    elif len(text) > 20:
        confidence += 0.1
    
    # Adjust based on character diversity
    unique_chars = len(set(text))
    if unique_chars > 20:
        confidence += 0.1
    
    # Boost confidence for non-Latin scripts (Indian languages)
    if detected_lang in ['hi', 'bn', 'te', 'ta', 'mr', 'gu', 'kn', 'ml', 'pa', 'or', 'as', 'ur', 'ne']:
        confidence += 0.1
    
    return min(confidence, 1.0)

def detect_and_translate(input_text: str, target_language: str = 'en') -> Tuple[str, str, float]:
    """
    Detect language and translate if needed using Groq model.
    
    Args:
        input_text: Text to process
        target_language: Target language for translation
        
    Returns:
        Tuple of (translated_text, detected_language, confidence)
    """
    detected_lang, confidence = detect_language_with_groq(input_text)
    
    # Log detection results
    logger.info(f"Detected language: {detected_lang} (confidence: {confidence:.2f})")
    
    # Translate if needed and confidence is high enough
    if detected_lang != target_language and confidence > 0.3:
        try:
            translator = GoogleTranslator(source='auto', target=target_language)
            translated_text = translator.translate(input_text)
            return translated_text, detected_lang, confidence
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return input_text, detected_lang, confidence
    
    return input_text, detected_lang, confidence

def translate_back(result_text: str, target_language: str) -> str:
    """
    Translate result back to target language.
    
    Args:
        result_text: Text to translate
        target_language: Target language
        
    Returns:
        Translated text
    """
    if target_language == 'en':
        return result_text
    
    try:
        translator = GoogleTranslator(source='en', target=target_language)
        return translator.translate(result_text)
    except Exception as e:
        logger.error(f"Back translation failed: {e}")
        return result_text

def get_supported_languages() -> list:
    """
    Get list of supported languages.
    """
    return [
        'en', 'hi', 'bn', 'te', 'ta', 'mr', 'gu', 'kn', 'ml', 'pa', 'or', 'as', 'ur', 'ne',
        'es', 'fr', 'de', 'it', 'pt', 'vi', 'id', 'ms', 'tl', 'th', 'my', 'km', 'lo', 'si'
    ]

def get_indian_languages() -> dict:
    """
    Get dictionary of supported Indian languages.
    
    Returns:
        Dictionary mapping language codes to names
    """
    return {
        'hi': 'Hindi',
        'hi_rom': 'Romanized Hindi',
        'bn': 'Bengali',
        'te': 'Telugu',
        'ta': 'Tamil',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'pa': 'Punjabi',
        'or': 'Odia',
        'as': 'Assamese',
        'ur': 'Urdu',
        'ne': 'Nepali'
    }

# Global instance for backward compatibility
class LanguageDetector:
    def __init__(self):
        pass
    
    def detect_language_enhanced(self, text: str) -> Tuple[str, float]:
        return detect_language_with_groq(text)
    
    def detect_and_translate(self, input_text: str, target_language: str = 'en') -> Tuple[str, str, float]:
        return detect_and_translate(input_text, target_language)
    
    def translate_back(self, result_text: str, target_language: str) -> str:
        return translate_back(result_text, target_language)
    
    def get_supported_languages(self) -> list:
        return get_supported_languages()

# Global instance
language_detector = LanguageDetector() 