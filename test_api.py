#!/usr/bin/env python3
"""
Simple test to verify API can start without problematic dependencies
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all imports work without sentence_transformers"""
    print("🔍 Testing imports...")
    
    try:
        # Test core imports
        from core.tarot_reader import perform_reading
        print("✅ core.tarot_reader imported successfully")
        
        from utils.language_detector import language_detector
        print("✅ utils.language_detector imported successfully")
        
        from utils.intent import classify_intent
        print("✅ utils.intent imported successfully")
        
        from utils.pdf_reader import TarotPDFEmbedder
        print("✅ utils.pdf_reader imported successfully")
        
        from core.rag import get_card_meaning
        print("✅ core.rag imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without starting the server"""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from utils.language_detector import language_detector
        from utils.intent import classify_intent
        from core.tarot_reader import perform_reading
        from utils.context import create_context
        
        # Test language detection
        lang, confidence = language_detector("Hello, how are you?")
        print(f"✅ Language detection: {lang} (confidence: {confidence:.2f})")
        
        # Test intent classification
        intent = classify_intent("What does my future hold?")
        print(f"✅ Intent classification: {intent}")
        
        # Test context creation
        context = create_context(language='en')
        print(f"✅ Context creation: {type(context)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing API Dependencies")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please check dependencies.")
        return False
    
    # Test basic functionality
    if not test_basic_functionality():
        print("\n❌ Basic functionality tests failed.")
        return False
    
    print("\n" + "=" * 40)
    print("✅ All tests passed!")
    print("🎉 Your API should now work without the problematic dependencies.")
    print("\n💡 You can now start your API with:")
    print("   uvicorn api:app --reload")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 