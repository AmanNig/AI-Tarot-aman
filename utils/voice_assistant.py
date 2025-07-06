import speech_recognition as sr
from gtts import gTTS
import os
import time
 
# Initialize the recognizer
recognizer = sr.Recognizer()

def listen_for_question():
    """
    Listens for a question from the user and converts speech to text.
    """
    with sr.Microphone() as source:
        print("🎤 Listening for your question... Speak now!")
        recognizer.adjust_for_ambient_noise(source)  # Adjust to ambient noise
        audio = recognizer.listen(source=source)

        try:
            question = recognizer.recognize_google(audio)
            print(f"🎧 You said: {question}")
            return question
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that. Can you please repeat?")
            return None
        except sr.RequestError:
            print("Could not connect to the service. Please try again later.")
            return None

def speak_response(response):
    """
    Converts text response to speech and plays it.
    """
    tts = gTTS(text=response, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")  # Plays the audio using mpg321 (Make sure mpg321 is installed)


# def voice_input_output_flow():
#     """
#     Initiates the voice interaction loop for asking questions and giving answers.
#     """
#     while True:
#         question = listen_for_question()
#         if question:
#             if "exit" in question.lower() or "quit" in question.lower():
#                 speak_response("Goodbye! Have a great day.")
#                 break

#             # Send question to perform_reading
#             response = "you are a student thank you"  # Update accordingly if needed
#             speak_response(response)

#         time.sleep(1)



# listen_for_question()