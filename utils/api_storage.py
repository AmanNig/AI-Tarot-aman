import requests
import json
import time
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lambda Function URL
LAMBDA_URL = "https://call-astro.com/api/ai-tool-analysis"

def store_tarot_response(
    session_number: str,
    time_duration: str,
    intent_type: str,
    question: str,
    answer: str,
    user_info: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Store tarot reading response in the Lambda API.
    
    Args:
        session_number: Session identifier
        time_duration: Duration of the session
        intent_type: Type of intent (general, timeline, etc.)
        question: User's question
        answer: Tarot reading response
        user_info: Optional user information dictionary
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Prepare the payload
        payload = {
            'session_number': session_number,
            'time_duration': time_duration,
            'intent_type': intent_type,
            'question': question,
            'answer': answer,
        }
        
        # Add user info if provided
        if user_info:
            payload.update({
                'user_name': user_info.get('name', ''),
                'user_dob': user_info.get('dob', ''),
                'user_birth_place': user_info.get('birth_place', ''),
                'user_birth_time': user_info.get('birth_time', ''),
                'user_gender': user_info.get('gender', ''),
                'user_mood': user_info.get('mood', ''),
                'user_day_summary': user_info.get('day_summary', ''),
            })
        
        # Make the API request
        response = requests.post(
            LAMBDA_URL,
            params=payload,
            timeout=30  # 30 second timeout
        )
        
        # Log the response
        logger.info(f"API Storage Status Code: {response.status_code}")
        
        if response.status_code == 200:
            logger.info("✅ SUCCESS! Response stored in Lambda API")
            return True
        else:
            logger.error(f"❌ FAILED! API returned status code: {response.status_code}")
            logger.error(f"Response content: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("❌ TIMEOUT! API request timed out after 30 seconds")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ REQUEST ERROR! {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ UNEXPECTED ERROR! {str(e)}")
        return False

def generate_session_number() -> str:
    """
    Generate a unique session number based on timestamp.
    
    Returns:
        str: Session number
    """
    return str(int(time.time()))

def calculate_duration(start_time: float) -> str:
    """
    Calculate duration from start time to now.
    
    Args:
        start_time: Start time as timestamp
        
    Returns:
        str: Duration in seconds
    """
    duration = time.time() - start_time
    return str(int(duration)) 