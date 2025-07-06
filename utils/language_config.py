"""
Configuration settings for language detection.
"""

# Supported languages and their configurations
SUPPORTED_LANGUAGES = {
    'en': {
        'name': 'English',
        'confidence_threshold': 0.3,
        'fallback': True
    },
    'hi': {
        'name': 'Hindi',
        'confidence_threshold': 0.3,
        'fallback': True
    },
    'hi_rom': {
        'name': 'Romanized Hindi',
        'confidence_threshold': 0.4,
        'fallback': True
    },
    'es': {
        'name': 'Spanish',
        'confidence_threshold': 0.3,
        'fallback': True
    },
    'fr': {
        'name': 'French',
        'confidence_threshold': 0.3,
        'fallback': True
    },
    'de': {
        'name': 'German',
        'confidence_threshold': 0.3,
        'fallback': True
    },
    'it': {
        'name': 'Italian',
        'confidence_threshold': 0.3,
        'fallback': True
    },
    'pt': {
        'name': 'Portuguese',
        'confidence_threshold': 0.3,
        'fallback': True
    }
}

# Language detection settings
DETECTION_SETTINGS = {
    'min_text_length': 1,
    'max_text_length': 10000,
    'default_language': 'en',
    'confidence_boost_long_text': 0.2,
    'confidence_penalty_ambiguous': 0.1,
    'confidence_boost_diversity': 0.1,
    'pattern_detection_threshold': 0.7,
    'short_text_confidence_multiplier': 0.8
}

# Translation settings
TRANSLATION_SETTINGS = {
    'max_retries': 3,
    'timeout_seconds': 10,
    'batch_size': 1,
    'preserve_formatting': True
}

# Logging settings
LOGGING_SETTINGS = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'log_detection_results': True,
    'log_translation_errors': True
}

# Performance settings
PERFORMANCE_SETTINGS = {
    'cache_detection_results': True,
    'cache_translation_results': True,
    'cache_ttl_seconds': 3600,  # 1 hour
    'max_cache_size': 1000
}

def get_language_config(language_code: str) -> dict:
    """
    Get configuration for a specific language.
    
    Args:
        language_code: Language code (e.g., 'en', 'hi', 'es')
        
    Returns:
        Language configuration dictionary
    """
    return SUPPORTED_LANGUAGES.get(language_code, SUPPORTED_LANGUAGES['en'])

def is_language_supported(language_code: str) -> bool:
    """
    Check if a language is supported.
    
    Args:
        language_code: Language code to check
        
    Returns:
        True if supported, False otherwise
    """
    return language_code in SUPPORTED_LANGUAGES

def get_supported_language_codes() -> list:
    """
    Get list of supported language codes.
    
    Returns:
        List of supported language codes
    """
    return list(SUPPORTED_LANGUAGES.keys())

def get_supported_language_names() -> dict:
    """
    Get mapping of language codes to names.
    
    Returns:
        Dictionary mapping language codes to names
    """
    return {code: config['name'] for code, config in SUPPORTED_LANGUAGES.items()} 