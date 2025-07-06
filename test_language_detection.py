#!/usr/bin/env python3
"""
Test script to demonstrate improved language detection capabilities.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.language_detector import language_detector, detect_and_translate
from langdetect import detect as original_detect

def test_language_detection():
    """Test various language detection scenarios."""
    
    test_cases = [
        # English tests
        ("Hello, how are you?", "en"),
        ("Will I find love?", "en"),
        ("What does my future hold?", "en"),
        
        # Hindi tests
        ("नमस्ते, कैसे हो आप?", "hi"),
        ("क्या मुझे प्यार मिलेगा?", "hi"),
        ("मेरा भविष्य कैसा होगा?", "hi"),
        
        # Spanish tests
        ("Hola, ¿cómo estás?", "es"),
        ("¿Encontraré el amor?", "es"),
        ("¿Qué me depara el futuro?", "es"),
        
        # French tests
        ("Bonjour, comment allez-vous?", "fr"),
        ("Vais-je trouver l'amour?", "fr"),
        ("Que me réserve l'avenir?", "fr"),
        
        # German tests
        ("Hallo, wie geht es dir?", "de"),
        ("Werde ich die Liebe finden?", "de"),
        ("Was hält die Zukunft für mich bereit?", "de"),
        
        # Italian tests
        ("Ciao, come stai?", "it"),
        ("Troverò l'amore?", "it"),
        ("Cosa mi riserva il futuro?", "it"),
        
        # Portuguese tests
        ("Olá, como você está?", "pt"),
        ("Vou encontrar o amor?", "pt"),
        ("O que o futuro me reserva?", "pt"),
        
        # Mixed language tests
        ("Hello नमस्ते", "en"),  # Should detect English as primary
        ("Hola hello", "es"),    # Should detect Spanish as primary
        ("Bonjour hello", "fr"), # Should detect French as primary
        
        # Short text tests
        ("Hi", "en"),
        ("नमस्ते", "hi"),
        ("Hola", "es"),
        ("Bonjour", "fr"),
        
        # Ambiguous text tests
        ("tarot card reading", "en"),
        ("love career money", "en"),
        ("future past present", "en"),
    ]
    
    print("🔮 Testing Improved Language Detection")
    print("=" * 50)
    
    improved_correct = 0
    original_correct = 0
    total_tests = len(test_cases)
    
    for i, (text, expected) in enumerate(test_cases, 1):
        print(f"\nTest {i}: '{text}'")
        print(f"Expected: {expected}")
        
        # Test improved detection
        try:
            detected_lang, confidence = language_detector.detect_language_enhanced(text)
            improved_result = "✅" if detected_lang == expected else "❌"
            print(f"Improved: {detected_lang} (confidence: {confidence:.2f}) {improved_result}")
            if detected_lang == expected:
                improved_correct += 1
        except Exception as e:
            print(f"Improved: Error - {e}")
        
        # Test original detection
        try:
            original_lang = original_detect(text)
            original_result = "✅" if original_lang == expected else "❌"
            print(f"Original: {original_lang} {original_result}")
            if original_lang == expected:
                original_correct += 1
        except Exception as e:
            print(f"Original: Error - {e}")
    
    print("\n" + "=" * 50)
    print("📊 RESULTS SUMMARY")
    print(f"Improved Detection Accuracy: {improved_correct}/{total_tests} ({improved_correct/total_tests*100:.1f}%)")
    print(f"Original Detection Accuracy: {original_correct}/{total_tests} ({original_correct/total_tests*100:.1f}%)")
    print(f"Improvement: +{improved_correct - original_correct} tests ({((improved_correct - original_correct)/total_tests)*100:.1f}%)")

def test_translation():
    """Test translation functionality."""
    
    print("\n🌐 Testing Translation Functionality")
    print("=" * 50)
    
    test_texts = [
        ("Hello, how are you?", "en"),
        ("नमस्ते, कैसे हो आप?", "hi"),
        ("Hola, ¿cómo estás?", "es"),
        ("Bonjour, comment allez-vous?", "fr"),
    ]
    
    for text, expected_lang in test_texts:
        print(f"\nOriginal ({expected_lang}): {text}")
        
        # Test detection and translation
        translated, detected_lang, confidence = language_detector.detect_and_translate(text)
        print(f"Detected: {detected_lang} (confidence: {confidence:.2f})")
        print(f"Translated to English: {translated}")
        
        # Test back translation
        if detected_lang != 'en':
            back_translated = language_detector.translate_back(translated, detected_lang)
            print(f"Back translated: {back_translated}")

def test_edge_cases():
    """Test edge cases and error handling."""
    
    print("\n⚠️ Testing Edge Cases")
    print("=" * 50)
    
    edge_cases = [
        "",  # Empty string
        "   ",  # Whitespace only
        "12345",  # Numbers only
        "!@#$%",  # Special characters only
        "a",  # Single character
        "tarot",  # Single word
        "नमस्ते कैसे हो आप क्या आप मुझे मेरे भविष्य के बारे में बता सकते हैं",  # Long Hindi text
    ]
    
    for text in edge_cases:
        print(f"\nInput: '{text}'")
        try:
            detected_lang, confidence = language_detector.detect_language_enhanced(text)
            print(f"Result: {detected_lang} (confidence: {confidence:.2f})")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_language_detection()
    test_translation()
    test_edge_cases()
    
    print("\n🎉 Language detection testing completed!") 