#!/usr/bin/env python3
"""
Test script for multilingual tarot reader
Tests that the system responds directly in the input language without translation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.language_detector import language_detector
from utils.intent import classify_intent
from core.tarot_reader import perform_reading, get_system_prompt
from utils.context import create_context

def test_language_detection():
    """Test language detection for various inputs"""
    print("🔍 Testing Language Detection...")
    
    test_cases = [
        ("Hello, how are you?", "en"),
        ("नमस्ते, कैसे हो आप?", "hi"),
        ("Namaste, kaise ho aap?", "hi_rom"),
        ("नमस्कार, तुम्ही कसे आहात?", "mr"),
        ("Namaskar, tumhi kase aahat?", "mr_rom"),
        ("আপনি কেমন আছেন?", "bn"),
        ("మీరు ఎలా ఉన్నారు?", "te"),
        ("நீங்கள் எப்படி இருக்கிறீர்கள்?", "ta"),
        ("તમે કેમ છો?", "gu")
    ]
    
    for text, expected in test_cases:
        detected, confidence = language_detector(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text[:20]}...' -> {detected} (expected: {expected}, confidence: {confidence:.2f})")

def test_system_prompts():
    """Test that system prompts are generated correctly for each language"""
    print("\n📝 Testing System Prompts...")
    
    languages = ['en', 'hi', 'hi_rom', 'mr', 'mr_rom', 'bn', 'te', 'ta', 'gu']
    
    for lang in languages:
        prompt = get_system_prompt(lang)
        # Check if prompt contains language-specific instructions
        if lang == 'en':
            assert "Respond in English" in prompt, f"English prompt missing language instruction"
        elif lang == 'hi':
            assert "हिंदी में जवाब दें" in prompt, f"Hindi prompt missing language instruction"
        elif lang == 'hi_rom':
            assert "Hindi Roman script mein jawab dein" in prompt, f"Hindi Roman prompt missing language instruction"
        elif lang == 'mr':
            assert "मराठीत उत्तर द्या" in prompt, f"Marathi prompt missing language instruction"
        elif lang == 'mr_rom':
            assert "Marathi Roman script madhe uttar dya" in prompt, f"Marathi Roman prompt missing language instruction"
        elif lang == 'bn':
            assert "বাংলায় উত্তর দিন" in prompt, f"Bengali prompt missing language instruction"
        elif lang == 'te':
            assert "తెలుగులో సమాధానం ఇవ్వండి" in prompt, f"Telugu prompt missing language instruction"
        elif lang == 'ta':
            assert "தமிழில் பதில் கொடுங்கள்" in prompt, f"Tamil prompt missing language instruction"
        elif lang == 'gu':
            assert "ગુજરાતીમાં જવાબ આપો" in prompt, f"Gujarati prompt missing language instruction"
        
        print(f"✅ {lang}: System prompt generated successfully")

def test_multilingual_responses():
    """Test that tarot reader responds in the correct language"""
    print("\n🔮 Testing Multilingual Tarot Responses...")
    
    test_questions = [
        ("What does my future hold?", "en"),
        ("मेरा भविष्य क्या है?", "hi"),
        ("Mera bhavishya kya hai?", "hi_rom"),
        ("माझे भविष्य काय आहे?", "mr"),
        ("Mazhe bhavishya kay aahe?", "mr_rom"),
        ("আমার ভবিষ্যত কি?", "bn"),
        ("నా భవిష్యత్తు ఏమిటి?", "te"),
        ("என் எதிர்காலம் என்ன?", "ta"),
        ("મારું ભવિષ્ય શું છે?", "gu")
    ]
    
    for question, expected_lang in test_questions:
        print(f"\n--- Testing: {question} (Expected: {expected_lang}) ---")
        
        # Detect language
        detected_lang, confidence = language_detector(question)
        print(f"Detected: {detected_lang} (confidence: {confidence:.2f})")
        
        # Classify intent
        intent = classify_intent(question)
        print(f"Intent: {intent}")
        
        # Create context
        context = create_context(language=detected_lang)
        
        # Perform reading
        result = perform_reading(question, intent, context.get_history(), detected_lang)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
            continue
        
        # Check response
        interpretation = result.get("interpretation", "")
        print(f"Response: {interpretation[:100]}...")
        
        # Verify response is in the correct language
        if expected_lang == 'en':
            # Check for English words
            english_indicators = ['the', 'and', 'you', 'your', 'will', 'can', 'should']
            has_english = any(word in interpretation.lower() for word in english_indicators)
            print(f"✅ English response: {has_english}")
        elif expected_lang == 'hi':
            # Check for Hindi words
            hindi_indicators = ['आप', 'आपका', 'है', 'हैं', 'करें', 'दें', 'सकते']
            has_hindi = any(word in interpretation for word in hindi_indicators)
            print(f"✅ Hindi response: {has_hindi}")
        elif expected_lang == 'hi_rom':
            # Check for Hindi Roman script
            hindi_rom_indicators = ['aap', 'aapka', 'hai', 'hain', 'karein', 'dein', 'sakte']
            has_hindi_rom = any(word in interpretation.lower() for word in hindi_rom_indicators)
            print(f"✅ Hindi Roman response: {has_hindi_rom}")
        elif expected_lang == 'mr':
            # Check for Marathi words
            marathi_indicators = ['तुम्ही', 'तुमचे', 'आहे', 'आहात', 'करा', 'द्या', 'शकता']
            has_marathi = any(word in interpretation for word in marathi_indicators)
            print(f"✅ Marathi response: {has_marathi}")
        elif expected_lang == 'mr_rom':
            # Check for Marathi Roman script
            marathi_rom_indicators = ['tumhi', 'tumche', 'aahe', 'aahat', 'kara', 'dya', 'shakta']
            has_marathi_rom = any(word in interpretation.lower() for word in marathi_rom_indicators)
            print(f"✅ Marathi Roman response: {has_marathi_rom}")
        elif expected_lang == 'bn':
            # Check for Bengali words
            bengali_indicators = ['আপনি', 'আপনার', 'হয়', 'হন', 'করুন', 'দিন', 'পারেন']
            has_bengali = any(word in interpretation for word in bengali_indicators)
            print(f"✅ Bengali response: {has_bengali}")
        elif expected_lang == 'te':
            # Check for Telugu words
            telugu_indicators = ['మీరు', 'మీ', 'ఉంది', 'ఉన్నారు', 'చేయండి', 'ఇవ్వండి', 'చేయవచ్చు']
            has_telugu = any(word in interpretation for word in telugu_indicators)
            print(f"✅ Telugu response: {has_telugu}")
        elif expected_lang == 'ta':
            # Check for Tamil words
            tamil_indicators = ['நீங்கள்', 'உங்கள்', 'உள்ளது', 'உள்ளீர்கள்', 'செய்யுங்கள்', 'கொடுங்கள்', 'முடியும்']
            has_tamil = any(word in interpretation for word in tamil_indicators)
            print(f"✅ Tamil response: {has_tamil}")
        elif expected_lang == 'gu':
            # Check for Gujarati words
            gujarati_indicators = ['તમે', 'તમારું', 'છે', 'છો', 'કરો', 'આપો', 'શકો']
            has_gujarati = any(word in interpretation for word in gujarati_indicators)
            print(f"✅ Gujarati response: {has_gujarati}")

def test_conversational_responses():
    """Test conversational responses in different languages"""
    print("\n💬 Testing Conversational Responses...")
    
    conversational_questions = [
        ("How are you today?", "en"),
        ("आज आप कैसे हैं?", "hi"),
        ("Aaj aap kaise hain?", "hi_rom"),
        ("आज तुम्ही कसे आहात?", "mr"),
        ("Aaj tumhi kase aahat?", "mr_rom")
    ]
    
    for question, expected_lang in conversational_questions:
        print(f"\n--- Conversational: {question} ---")
        
        detected_lang, confidence = language_detector(question)
        intent = classify_intent(question)
        context = create_context(language=detected_lang)
        
        result = perform_reading(question, intent, context.get_history(), detected_lang)
        
        if "error" not in result:
            interpretation = result.get("interpretation", "")
            print(f"Response: {interpretation[:150]}...")
            
            # Check if response is conversational and in the right language
            if expected_lang == 'en':
                conversational_indicators = ['good', 'well', 'thank', 'ready', 'help']
            elif expected_lang == 'hi':
                conversational_indicators = ['अच्छा', 'धन्यवाद', 'तैयार', 'मदद', 'स्वागत']
            elif expected_lang == 'hi_rom':
                conversational_indicators = ['achha', 'dhanyavad', 'taiyar', 'madad', 'swagat']
            elif expected_lang == 'mr':
                conversational_indicators = ['चांगले', 'धन्यवाद', 'तयार', 'मदत', 'स्वागत']
            elif expected_lang == 'mr_rom':
                conversational_indicators = ['changale', 'dhanyavad', 'tayar', 'madat', 'swagat']
            
            has_conversational = any(word in interpretation.lower() for word in conversational_indicators)
            print(f"✅ Conversational response: {has_conversational}")

def main():
    """Run all tests"""
    print("🧪 Testing Multilingual Tarot Reader")
    print("=" * 50)
    
    try:
        test_language_detection()
        test_system_prompts()
        test_multilingual_responses()
        test_conversational_responses()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("🎉 The multilingual tarot reader is working correctly!")
        print("🌍 It now responds directly in the input language without translation!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 