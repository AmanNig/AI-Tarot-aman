#!/usr/bin/env python3
"""
Test script for transliterated language detection
"""

from utils.language_detector import detect_language_with_groq, detect_and_translate

def test_transliterated_languages():
    """Test various transliterated language inputs"""
    
    test_cases = [
        # Hindi in Roman script
        ("mai aj kya kru?", "hi_rom"),
        ("mujhe yeh pasand hai", "hi_rom"),
        ("kya haal hai dost?", "hi_rom"),
        ("main kal office jaunga", "hi_rom"),
        
        # Marathi in Roman script
        ("mi aaj kay karaycha?", "mr_rom"),
        ("mala hee ghadaycha aahe", "mr_rom"),
        ("kuthe jaat aahat?", "mr_rom"),
        ("mi udya office la jaat aahe", "mr_rom"),
        
        # Bengali in Roman script
        ("ami aj ki korbo?", "bn_rom"),
        ("amar nam ki?", "bn_rom"),
        ("kothay jaccho?", "bn_rom"),
        ("kemon acho?", "bn_rom"),
        
        # Telugu in Roman script
        ("naanu ee em chestha?", "te_rom"),
        ("naku ee pani kavali", "te_rom"),
        ("ekkada veltunnavu?", "te_rom"),
        ("elaa unnaru?", "te_rom"),
        
        # Tamil in Roman script
        ("naan inru enna seiven?", "ta_rom"),
        ("enakku ee velai venum", "ta_rom"),
        ("enge poren?", "ta_rom"),
        ("eppadi irukkinga?", "ta_rom"),
        
        # Gujarati in Roman script
        ("hu aaj shu karish?", "gu_rom"),
        ("mari naam kya che?", "gu_rom"),
        ("kya jao cho?", "gu_rom"),
        ("kem cho?", "gu_rom"),
        
        # Mixed languages (should default to the dominant one)
        ("mai aaj kay karu?", "hi_rom"),
        ("mujhe kuthe jaana hai?", "hi_rom"),
        
        # English
        ("Hello, how are you?", "en"),
        ("What is your name?", "en"),
        
        # Native Hindi
        ("नमस्ते, कैसे हो आप?", "hi"),
        ("मैं कल ऑफिस जाऊंगा", "hi"),
        
        # Native Marathi
        ("नमस्कार, कसे आहात?", "mr"),
        ("मी उद्या ऑफिस ला जात आहे", "mr"),
        
        # Native Bengali
        ("নমস্কার, কেমন আছেন?", "bn"),
        ("আমি কাল অফিসে যাব", "bn"),
        
        # Native Telugu
        ("నమస్కారం, ఎలా ఉన్నారు?", "te"),
        ("నేను రేపు ఆఫీస్ కి వెళ్తాను", "te"),
        
        # Native Tamil
        ("வணக்கம், எப்படி இருக்கிறீர்கள்?", "ta"),
        ("நான் நாளை அலுவலகம் போகிறேன்", "ta"),
        
        # Native Gujarati
        ("નમસ્કાર, કેમ છો?", "gu"),
        ("હું કાલે ઓફિસ જઈશ", "gu"),
    ]
    
    print("Testing Transliterated Language Detection")
    print("=" * 50)
    
    for text, expected in test_cases:
        detected_lang, confidence = detect_language_with_groq(text)
        status = "✅" if detected_lang == expected else "❌"
        print(f"{status} Text: '{text}'")
        print(f"   Expected: {expected}, Detected: {detected_lang}, Confidence: {confidence:.2f}")
        print()
    
    print("\nTesting Translation Pipeline")
    print("=" * 50)
    
    # Test translation pipeline
    test_translations = [
        "mai aj kya kru?",
        "mi aaj kay karaycha?",
        "ami aj ki korbo?",
        "naanu ee em chestha?",
        "naan inru enna seiven?",
        "hu aaj shu karish?",
        "kya haal hai dost?",
        "kuthe jaat aahat?",
    ]
    
    for text in test_translations:
        translated, detected_lang, confidence = detect_and_translate(text, 'en')
        print(f"Original: '{text}'")
        print(f"Detected: {detected_lang} (confidence: {confidence:.2f})")
        print(f"Translated: '{translated}'")
        print()

if __name__ == "__main__":
    test_transliterated_languages() 