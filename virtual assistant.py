import pyttsx3
import speech_recognition as sr
import pywhatkit
import datetime
import webbrowser
import os
#import serial
import time
import requests
from dotenv import load_dotenv
import google.generativeai as genai

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
generation_config = {
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 50,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}
model = genai.GenerativeModel(
    model_name="gemini-2.0",
    generation_config=generation_config,
    system_instruction="You are a helpful virtual assistant."
)

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to take voice input
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Could you repeat?")
            return None
        except sr.RequestError:
            speak("Could not request results; check your internet connection.")
            return None

# Function to execute commands
def execute_command(command, chat_history):
    if 'search website' in command:
        speak("What should I search for?")
        query = take_command()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            speak(f"Here are the results for {query}.")

    elif 'play' in command:
        speak("What should I play?")
        video = take_command()
        if video:
            pywhatkit.playonyt(video)
            speak(f"Playing {video} on YouTube.")

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        speak(f"The time is {current_time}.")

    elif 'date' in command:
        current_date = datetime.datetime.now().strftime('%B %d, %Y')
        speak(f"Today's date is {current_date}.")

    elif 'ask gemini' in command or 'ai assistant' in command:
        speak("What should I ask Gemini?")
        query = take_command()
        if query:
            chat_session = model.start_chat(history=chat_history)
            response = chat_session.send_message(query)
            gemini_response = response.text
            speak(f"Gemini says: {gemini_response}")
            chat_history.append({"role": "user", "parts": query})
            chat_history.append({"role": "model", "parts": gemini_response})

    elif 'quit' in command or 'exit' in command:
        speak("Goodbye!")
        exit()

# Main loop
def main():
    # connection_state = False
    # serial_connection = None
    chat_history = []

    # try:
    #     serial_connection = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    #     connection_state = True
    #     speak("Device connected. I am ready to assist you.")
    # except Exception as e:
    #     speak("Device not connected. Operating without hardware integration.")

    speak("Hello! I am your virtual assistant. How can I help you today?")
    while True:
        command = take_command()
        if command:
            execute_command(command, chat_history)

# Run the assistant
if __name__ == "__main__":
    main()
