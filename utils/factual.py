# factual.py

import wikipedia

def answer_factual(question: str) -> str:
    """
    Try to fetch a concise summary from Wikipedia.
    If that fails, return a polite error.
    """
    try:
        # Get the first two sentences of the relevant page
        return wikipedia.summary(question, sentences=2)
    except Exception as e:
        return f"Sorry, I couldn’t find a clear answer for that. ({e})"
