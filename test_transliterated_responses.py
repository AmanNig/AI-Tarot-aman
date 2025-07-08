#!/usr/bin/env python3
"""
Test script for transliterated response system
"""

from utils.language_detector import detect_and_translate, translate_back
from utils.intent import classify_intent
from core.tarot_reader import perform_reading
from utils.context import create_context

def test_transliterated_responses():
    """Test that responses are in the same transliterated format as input"""
    
    test_cases = [
        # Hindi in Roman script
        ("mai aj kya kru?", "hi_rom"),
        ("mujhe yeh pasand hai", "hi_rom"),
        ("kya haal hai dost?", "hi_rom"),
        
        # Marathi in Roman script
        ("mi aaj kay karaycha?", "mr_rom"),
        ("mala hee ghadaycha aahe", "mr_rom"),
        ("kuthe jaat aahat?", "mr_rom"),
        
        # Bengali in Roman script
        ("ami aj ki korbo?", "bn_rom"),
        ("amar nam ki?", "bn_rom"),
        ("kothay jaccho?", "bn_rom"),
        
        # Telugu in Roman script
        ("naanu ee em chestha?", "te_rom"),
        ("naku ee pani kavali", "te_rom"),
        ("ekkada veltunnavu?", "te_rom"),
        
        # Tamil in Roman script
        ("naan inru enna seiven?", "ta_rom"),
        ("enakku ee velai venum", "ta_rom"),
        ("enge poren?", "ta_rom"),
        
        # Gujarati in Roman script
        ("hu aaj shu karish?", "gu_rom"),
        ("mari naam kya che?", "gu_rom"),
        ("kya jao cho?", "gu_rom"),
    ]
    
    print("Testing Transliterated Response System")
    print("=" * 60)
    
    for question, expected_lang in test_cases:
        print(f"\n🔍 Testing: '{question}'")
        print(f"Expected language: {expected_lang}")
        
        # Create context
        context = create_context(language=expected_lang)
        
        # Detect and translate
        translated_q, detected_lang, confidence = detect_and_translate(question, target_language='en')
        print(f"Detected: {detected_lang} (confidence: {confidence:.2f})")
        
        # Classify intent
        intent = classify_intent(translated_q)
        print(f"Intent: {intent}")
        
        # Perform reading
        result = perform_reading(translated_q, intent, context.get_history())
        
        # Build result text
        if intent == "factual":
            result_text = "Sorry, I cannot provide factual information at the moment. Please ask a tarot-related question."
        elif intent == "conversation":
            result_text = result["interpretation"]
        else:
            if cards := result.get("cards"):
                result_text = f"Cards Drawn: {', '.join(cards)}\n\n{result['interpretation']}"
            else:
                result_text = result["interpretation"]
        
        # Translate back to transliterated format
        if detected_lang.endswith('_rom'):
            transliterated_response = translate_back(result_text, detected_lang)
            print(f"✅ Transliterated Response ({detected_lang}):")
            print(f"   {transliterated_response[:200]}...")
            
            # Check if response contains transliterated words
            if any(word in transliterated_response.lower() for word in ['mai', 'mi', 'ami', 'naanu', 'naan', 'hu']):
                print("✅ Response appears to be in transliterated format")
            else:
                print("⚠️ Response may not be in transliterated format")
        else:
            print(f"❌ Expected {expected_lang} but detected {detected_lang}")
        
        print("-" * 60)

def test_specific_hindi_rom():
    """Test specific Hindi Roman case mentioned by user"""
    
    print("\n🎯 Testing Specific Case: 'mai aj kya kru'")
    print("=" * 60)
    
    question = "mai aj kya kru"
    context = create_context(language='hi_rom')
    
    # Detect and translate
    translated_q, detected_lang, confidence = detect_and_translate(question, target_language='en')
    print(f"Question: '{question}'")
    print(f"Detected: {detected_lang} (confidence: {confidence:.2f})")
    print(f"Translated: '{translated_q}'")
    
    # Classify intent
    intent = classify_intent(translated_q)
    print(f"Intent: {intent}")
    
    # Perform reading
    result = perform_reading(translated_q, intent, context.get_history())
    
    # Build result text
    if cards := result.get("cards"):
        result_text = f"Cards Drawn: {', '.join(cards)}\n\n{result['interpretation']}"
    else:
        result_text = result["interpretation"]
    
    print(f"\nEnglish Response:")
    print(f"{result_text[:300]}...")
    
    # Translate back to Hindi Roman
    if detected_lang == 'hi_rom':
        transliterated_response = translate_back(result_text, 'hi_rom')
        print(f"\n✅ Hindi Roman Response:")
        print(f"{transliterated_response[:300]}...")
        
        # Check for transliterated indicators
        transliterated_indicators = ['mai', 'aap', 'kya', 'kar', 'hai', 'mein', 'ko', 'ka', 'ki', 'ke']
        found_indicators = [word for word in transliterated_indicators if word in transliterated_response.lower()]
        print(f"\nFound transliterated words: {found_indicators}")
        
        if found_indicators:
            print("✅ Response is in Hindi Roman format!")
        else:
            print("⚠️ Response may not be in proper Hindi Roman format")
    else:
        print(f"❌ Expected hi_rom but detected {detected_lang}")

if __name__ == "__main__":
    test_transliterated_responses()
    test_specific_hindi_rom() 