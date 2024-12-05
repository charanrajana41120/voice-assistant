import pyttsx3
import speech_recognition as sr
import datetime
import os
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import pywhatkit as kit
import smtplib
import sys
import time
import pyjokes
import requests
import pyautogui
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import langdetect

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[len(voices) - 1].id)

# Text to speech function
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Convert voice to text function with retry mechanism
def take_command(language='en', retries=3):
    r = sr.Recognizer()
    for attempt in range(retries):
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            try:
                audio = r.listen(source, timeout=5, phrase_time_limit=8)
                print("Recognizing...")
                query = r.recognize_google(audio, language=language)
                print(f"User said: {query}")
                return query
            except sr.WaitTimeoutError:
                speak("Listening timed out while waiting for phrase to start.")
            except sr.UnknownValueError:
                speak("Google Speech Recognition could not understand the audio.")
            except sr.RequestError as e:
                speak(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(e)
                speak("Say that again please...")
    
    speak("Sorry, I could not understand. Please try again later.")
    return "none"

# Detect language function
def detect_language(text):
    try:
        detected_language = langdetect.detect(text)
        return detected_language
    except Exception as e:
        print(f"Language detection error: {e}")
        return 'en'  # Default to English if detection fails

# Wish the user function
def wish():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")

    if hour >= 0 and hour <= 12:
        speak(f"Good morning, it's {tt}")
    elif hour >= 12 and hour <= 18:
        speak(f"Good afternoon, it's {tt}")
    else:
        speak(f"Good evening, it's {tt}")
    speak("I am Jarvis sir. Please tell me how may I help you")

# Send email function
def send_email(to, subject, message, file_location=None):
    email = 'charan.rajana007@gmail.com'  # Replace with your email address
    password = 'sncv xyqn vnop njql'  # Replace with your email password
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    if file_location:
        filename = os.path.basename(file_location)
        with open(file_location, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f"attachment; filename={filename}")
            msg.attach(part)

    text = msg.as_string()
    server.sendmail(email, to, text)
    server.quit()

# Fetch news function
def news():
    api_key = "cad2a8eee1404971b4add17afc84357f"  # Replace with your API key
    main_url = f'http://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey={api_key}'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head = []
    day = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "tenth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range(len(day)):
        speak(f"Today's {day[i]} news is: {head[i]}")

# Load contacts function
def load_contacts(filename='contacts/contacts.txt'):
    contacts = {}
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                if line.strip():  # Ignore empty lines
                    name, number = line.strip().split(',')
                    contacts[name.lower()] = number
    return contacts

# Send WhatsApp message function
def send_whatsapp_message(name, message, wait_seconds=10):
    contacts = load_contacts()
    phone_number = contacts.get(name.lower())
    
    if not phone_number:
        speak(f"No contact found for {name}.")
        return

    # Ensure the wait time is sufficient
    if wait_seconds < 20:
        wait_seconds = 20  # Minimum wait time to allow WhatsApp Web to load

    speak(f"I will send the message to {name} in {wait_seconds} seconds.")
    time.sleep(wait_seconds)  # Wait for the specified delay

    # Calculate the time to send the message
    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(seconds=15)  # Additional 15 seconds buffer
    
    hour = send_time.hour
    minute = send_time.minute

    # Ensure the time is valid for WhatsApp scheduling
    if minute == 60:
        minute = 0
        hour += 1
        if hour == 24:
            hour = 0

    # Use the current minute and next minute if sending immediately
    if minute < now.minute:
        hour += 1
        minute = now.minute

    # Sending the message
    try:
        kit.sendwhatmsg(phone_number, message, hour, minute)
        speak(f"Message has been scheduled to be delivered at {hour}:{minute:02d}.")
    except Exception as e:
        speak(f"An error occurred: {e}")

# Search Wikipedia function
def search_wikipedia(query):
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    except wikipedia.exceptions.DisambiguationError as e:
        speak("The search term was ambiguous. Please be more specific.")
    except wikipedia.exceptions.PageError as e:
        speak("No page found for the search term.")
    except wikipedia.exceptions.WikipediaException as e:
        speak(f"An error occurred: {e}")

# Main program
if __name__ == "__main__":
    wish()
    while True:
        query = take_command().lower()

        # Detect language
        detected_language = detect_language(query)
        language = 'en' if detected_language == 'en' else 'te-IN'

        # Logic building for tasks
        if query == "none":
            continue

        if "open notepad" in query:
            npath = "C:\\Windows\\system32\\notepad.exe"
            os.startfile(npath)
        
        elif 'hi' in query or 'hello' in query:
            speak('Hello sir, how may I help you?')
        
        elif "open adobe reader" in query:
            apath = "C:\\Program Files (x86)\\Adobe\\Reader 11.0\\Reader\\AcroRd32.exe"
            os.startfile(apath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('webcam', img)
                k = cv2.waitKey(50)
                if k == 27:
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif "play music" in query:
            music_dir = "E:\\music"
            songs = os.listdir(music_dir)
            for song in songs:
                if song.endswith('.mp3'):
                    os.startfile(os.path.join(music_dir, song))

        elif "ip address" in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")

        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")

        elif "open stackoverflow" in query:
            webbrowser.open("www.stackoverflow.com")

        elif "open google" in query:
            speak("Sir, what should I search on Google")
            cm = take_command(language).lower()
            webbrowser.open(f"{cm}")

        elif "send whatsapp message" in query:
            speak("Please provide the name of the contact")
            name = take_command(language).strip()
            if name == "none":
                continue
            speak("What message should I send?")
            message = take_command(language).strip()
            if message != "none":
                send_whatsapp_message(name, message)
            else:
                speak("Message not recognized, please try again.")

        elif "email with file to avinash" in query:
            try:
                speak("Sir, what is the subject for this email")
                subject = take_command(language).lower()
                speak("And sir, what is the message for this email")
                message = take_command(language).lower()
                speak("Sir please enter the correct path of the file into the shell")
                file_location = input("Please enter the path here: ")
                to = "recipient@example.com"  # Replace with the actual recipient email
                send_email(to, subject, message, file_location)
                speak("Email with the file has been sent to Avinash")
            except Exception as e:
                print(e)
                speak("Sorry sir, I am not able to send this email with the file to Avinash")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "shut down the system" in query:
            os.system("shutdown /s /t 5")

        elif "restart the system" in query:
            os.system("shutdown /r /t 5")

        elif "sleep the system" in query:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

        elif 'switch the window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        elif "tell me news" in query:
            speak("Please wait sir, fetching the latest news")
            news()

        elif "no thanks" in query:
            speak("Thanks for using me sir, have a good day.")
            sys.exit()

        elif "close notepad" in query:
            speak("Okay sir, closing Notepad")
            os.system("taskkill /f /im notepad.exe")

        elif "set alarm" in query:
            nn = int(datetime.datetime.now().hour)
            if nn == 22:
                music_dir = 'E:\\music'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))

        # Add any additional commands as needed
