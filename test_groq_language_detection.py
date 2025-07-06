#!/usr/bin/env python3
"""
Test script to demonstrate Groq-based language detection for Indian languages.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.language_detector import detect_language_with_groq, detect_and_translate, get_indian_languages

def test_indian_language_detection():
    """Test Groq-based language detection for Indian languages."""
    
    # Test cases for Indian languages
    test_cases = [
        # Hindi
        ("नमस्ते, कैसे हो आप?", "hi"),
        ("क्या मुझे प्यार मिलेगा?", "hi"),
        ("मेरा भविष्य कैसा होगा?", "hi"),
        ("मैं अपनी नौकरी में सफल होऊंगा?", "hi"),
        
        # Romanized Hindi
        ("mai aj kya kru?", "hi_rom"),
        ("kya haal hai?", "hi_rom"),
        ("mujhe pyar milega?", "hi_rom"),
        ("mera future kaisa hoga?", "hi_rom"),
        ("main apni job mein successful hoga?", "hi_rom"),
        ("aaj ka din kaisa rahega?", "hi_rom"),
        ("kya main apne dost se milunga?", "hi_rom"),
        ("meri shaadi kab hogi?", "hi_rom"),
        
        # Bengali
        ("নমস্কার, কেমন আছেন?", "bn"),
        ("আমি কি ভালোবাসা পাব?", "bn"),
        ("আমার ভবিষ্যৎ কেমন হবে?", "bn"),
        ("আমি কি আমার ক্যারিয়ারে সফল হব?", "bn"),
        
        # Telugu
        ("నమస్కారం, ఎలా ఉన్నారు?", "te"),
        ("నాకు ప్రేమ వస్తుందా?", "te"),
        ("నా భవిష్యత్తు ఎలా ఉంటుంది?", "te"),
        ("నేను నా కెరీర్‌లో విజయవంతం అవుతానా?", "te"),
        
        # Tamil
        ("வணக்கம், எப்படி இருக்கிறீர்கள்?", "ta"),
        ("எனக்கு காதல் கிடைக்குமா?", "ta"),
        ("என் எதிர்காலம் எப்படி இருக்கும்?", "ta"),
        ("நான் என் தொழிலில் வெற்றி பெறுவேனா?", "ta"),
        
        # Marathi
        ("नमस्कार, कसे आहात?", "mr"),
        ("मला प्रेम मिळेल का?", "mr"),
        ("माझे भविष्य कसे असेल?", "mr"),
        ("मी माझ्या करिअरमध्ये यशस्वी होईन का?", "mr"),
        
        # Gujarati
        ("નમસ્તે, કેમ છો?", "gu"),
        ("મને પ્રેમ મળશે?", "gu"),
        ("મારું ભવિષ્ય કેવું રહેશે?", "gu"),
        ("હું મારી કારકિર્દીમાં સફળ થઈશ?", "gu"),
        
        # Kannada
        ("ನಮಸ್ಕಾರ, ಹೇಗೆ ಇದ್ದೀರಿ?", "kn"),
        ("ನನಗೆ ಪ್ರೀತಿ ಸಿಗುತ್ತದೆಯೇ?", "kn"),
        ("ನನ್ನ ಭವಿಷ್ಯ ಹೇಗೆ ಇರುತ್ತದೆ?", "kn"),
        ("ನಾನು ನನ್ನ ವೃತ್ತಿಜೀವನದಲ್ಲಿ ಯಶಸ್ವಿಯಾಗುತ್ತೇನೆ?", "kn"),
        
        # Malayalam
        ("നമസ്കാരം, എങ്ങനെ ഉണ്ട്?", "ml"),
        ("എനിക്ക് സ്നേഹം ലഭിക്കുമോ?", "ml"),
        ("എന്റെ ഭാവി എങ്ങനെ ആയിരിക്കും?", "ml"),
        ("ഞാൻ എന്റെ കരിയറിൽ വിജയിക്കുമോ?", "ml"),
        
        # Punjabi
        ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਕਿਵੇਂ ਹੋ?", "pa"),
        ("ਮੈਨੂੰ ਪਿਆਰ ਮਿਲੇਗਾ?", "pa"),
        ("ਮੇਰਾ ਭਵਿੱਖ ਕਿਵੇਂ ਹੋਵੇਗਾ?", "pa"),
        ("ਮੈਂ ਆਪਣੇ ਕੈਰੀਅਰ ਵਿੱਚ ਸਫਲ ਹੋਵਾਂਗਾ?", "pa"),
        
        # Odia
        ("ନମସ୍କାର, କିପରି ଅଛନ୍ତି?", "or"),
        ("ମୋତେ ପ୍ରେମ ମିଳିବ?", "or"),
        ("ମୋ ଭବିଷ୍ୟତ କିପରି ହେବ?", "or"),
        ("ମୁଁ ମୋ କ୍ୟାରିଅରରେ ସଫଳ ହେବି?", "or"),
        
        # Assamese
        ("নমস্কাৰ, কেনেকৈ আছা?", "as"),
        ("মোক মৰম পাম নেকি?", "as"),
        ("মোৰ ভৱিষ্যত কেনেকুৱা হ'ব?", "as"),
        ("মই মোৰ কৰ্মজীৱনত সফল হ'ম নেকি?", "as"),
        
        # Urdu
        ("السلام علیکم، کیسے ہیں؟", "ur"),
        ("کیا مجھے محبت ملے گی؟", "ur"),
        ("میرا مستقبل کیسا ہوگا؟", "ur"),
        ("کیا میں اپنے کیریئر میں کامیاب ہوں گا؟", "ur"),
        
        # Nepali
        ("नमस्ते, कसरी हुनुहुन्छ?", "ne"),
        ("मलाई माया मिल्छ?", "ne"),
        ("मेरो भविष्य कस्तो हुनेछ?", "ne"),
        ("म मेरो करियरमा सफल हुनेछु?", "ne"),
        
        # English (for comparison)
        ("Hello, how are you?", "en"),
        ("Will I find love?", "en"),
        ("What does my future hold?", "en"),
        ("Will I be successful in my career?", "en"),
    ]
    
    print("🔮 Testing Groq-Based Language Detection for Indian Languages")
    print("=" * 70)
    
    correct_detections = 0
    total_tests = len(test_cases)
    
    for i, (text, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{text}'")
        print(f"Expected: {expected}")
        
        try:
            detected_lang, confidence = detect_language_with_groq(text)
            result = "✅" if detected_lang == expected else "❌"
            print(f"Detected: {detected_lang} (confidence: {confidence:.2f}) {result}")
            
            if detected_lang == expected:
                correct_detections += 1
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 70)
    print("📊 RESULTS SUMMARY")
    print(f"Total Tests: {total_tests}")
    print(f"Correct Detections: {correct_detections}")
    print(f"Accuracy: {correct_detections/total_tests*100:.1f}%")
    
    # Show Indian languages supported
    indian_langs = get_indian_languages()
    print(f"\n🇮🇳 Supported Indian Languages: {len(indian_langs)}")
    for code, name in indian_langs.items():
        print(f"  • {code}: {name}")

def test_translation_functionality():
    """Test translation functionality with Indian languages."""
    
    print("\n🌐 Testing Translation Functionality")
    print("=" * 50)
    
    test_texts = [
        ("नमस्ते, कैसे हो आप?", "hi"),
        ("নমস্কার, কেমন আছেন?", "bn"),
        ("నమస్కారం, ఎలా ఉన్నారు?", "te"),
        ("வணக்கம், எப்படி இருக்கிறீர்கள்?", "ta"),
    ]
    
    for text, expected_lang in test_texts:
        print(f"\nOriginal ({expected_lang}): {text}")
        
        # Test detection and translation
        translated, detected_lang, confidence = detect_and_translate(text)
        print(f"Detected: {detected_lang} (confidence: {confidence:.2f})")
        print(f"Translated to English: {translated}")
        
        # Test back translation
        if detected_lang != 'en':
            from utils.language_detector import translate_back
            back_translated = translate_back(translated, detected_lang)
            print(f"Back translated: {back_translated}")

def test_short_texts():
    """Test detection with very short texts."""
    
    print("\n📝 Testing Short Text Detection")
    print("=" * 50)
    
    short_texts = [
        ("नमस्ते", "hi"),
        ("নমস্কার", "bn"),
        ("నమస్కారం", "te"),
        ("வணக்கம்", "ta"),
        ("नमस्कार", "mr"),
        ("નમસ્તે", "gu"),
        ("ನಮಸ್ಕಾರ", "kn"),
        ("നമസ്കാരം", "ml"),
        ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", "pa"),
        ("ନମସ୍କାର", "or"),
        ("নমস্কাৰ", "as"),
        ("السلام علیکم", "ur"),
        ("नमस्ते", "ne"),
    ]
    
    for text, expected in short_texts:
        print(f"\nText: '{text}'")
        try:
            detected_lang, confidence = detect_language_with_groq(text)
            result = "✅" if detected_lang == expected else "❌"
            print(f"Expected: {expected}, Detected: {detected_lang} (confidence: {confidence:.2f}) {result}")
        except Exception as e:
            print(f"Error: {e}")

def test_romanized_hindi_detection():
    """Test Romanized Hindi detection specifically."""
    
    print("\n🔤 Testing Romanized Hindi Detection")
    print("=" * 50)
    
    romanized_hindi_tests = [
        ("mai aj kya kru?", "hi_rom"),
        ("kya haal hai?", "hi_rom"),
        ("mujhe pyar milega?", "hi_rom"),
        ("mera future kaisa hoga?", "hi_rom"),
        ("main apni job mein successful hoga?", "hi_rom"),
        ("aaj ka din kaisa rahega?", "hi_rom"),
        ("kya main apne dost se milunga?", "hi_rom"),
        ("meri shaadi kab hogi?", "hi_rom"),
        ("mujhe paise milege?", "hi_rom"),
        ("kya main accha hoga?", "hi_rom"),
        ("mera naam kya hai?", "hi_rom"),
        ("ghar mein kya chal raha hai?", "hi_rom"),
        ("kaam kaisa chal raha hai?", "hi_rom"),
        ("dost se milne ja raha hoon", "hi_rom"),
        ("pyar mein kya hoga?", "hi_rom"),
        ("shaadi kab hogi?", "hi_rom"),
        ("naukri milegi?", "hi_rom"),
        ("paise kahan se aayenge?", "hi_rom"),
        ("samay kaisa hai?", "hi_rom"),
        ("roz kya karta hai?", "hi_rom"),
        ("kal kya hoga?", "hi_rom"),
        ("parso kya plan hai?", "hi_rom"),
    ]
    
    correct_detections = 0
    total_tests = len(romanized_hindi_tests)
    
    for i, (text, expected) in enumerate(romanized_hindi_tests, 1):
        print(f"\nTest {i}: '{text}'")
        print(f"Expected: {expected}")
        
        try:
            detected_lang, confidence = detect_language_with_groq(text)
            result = "✅" if detected_lang == expected else "❌"
            print(f"Detected: {detected_lang} (confidence: {confidence:.2f}) {result}")
            
            if detected_lang == expected:
                correct_detections += 1
                
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("📊 ROMANIZED HINDI RESULTS")
    print(f"Total Tests: {total_tests}")
    print(f"Correct Detections: {correct_detections}")
    print(f"Accuracy: {correct_detections/total_tests*100:.1f}%")

if __name__ == "__main__":
    test_indian_language_detection()
    test_romanized_hindi_detection()
    test_translation_functionality()
    test_short_texts()
    
    print("\n🎉 Groq-based language detection testing completed!")
    print("\n💡 Key Features:")
    print("  • Uses the same Groq model as intent classification and tarot reading")
    print("  • Supports 13 major Indian languages + Romanized Hindi")
    print("  • Provides confidence scores for each detection")
    print("  • Includes fallback pattern detection for reliability")
    print("  • Maintains backward compatibility with existing code")
    print("  • NEW: Romanized Hindi (hi_rom) for informal Hindi chat") 