import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
import datetime
import pyjokes

# initialize recognizer and speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print("You said:", command)
            return command
    except Exception as e:
        print("Error:", e)
        return ""

def wake_word_detected(command):
    return 'assistant' in command or 'buddy' in command

def run_ai():
    command = take_command()

    if 'youtube' in command:
        talk("Opening YouTube ")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        talk("Opening Google ")
        webbrowser.open("https://www.google.com")

    elif 'search' in command:
        search_query = command.replace('search', '').strip()
        talk(f"Searching for {search_query} ")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    elif 'play' in command:
        song = command.replace('play', '').strip()
        talk(f'Playing {song} ')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {time} ")

    elif 'instagram' in command:
        talk("Opening Instagram 📸")
        webbrowser.open("https://www.instagram.com")

    elif 'github' in command or 'git hub' in command:
        talk("Opening GitHub ")
        webbrowser.open("https://github.com")

    elif 'joke' in command:
        joke = pyjokes.get_joke()
        talk(joke)

    elif 'exit' in command or 'stop' in command:
        talk("Okay byeee !")
        return False

    else:
        talk("Sorry, I didn't get that.")
        return False  # Stop if not understood

    return True  # Continue listening

# main loop
talk("Say 'hello assistant' to wake me up 🔊")
while True:
    wake_command = take_command()
    print(f"DEBUG: Wake command recognized: '{wake_command}'")
    if not wake_command:
        talk("I didn't hear anything. Please try again.")
        continue
    if wake_word_detected(wake_command):
        talk("Yes, I'm here. Tell me what to do ")
        if not run_ai():
            break

print(sr.Microphone.list_microphone_names())
