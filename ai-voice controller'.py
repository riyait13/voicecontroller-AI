import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser

# Initialize the recognizer and speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set voice to female/male (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 = male, 1 = female


def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening... 🎧")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print("You said: " + command)
            return command
    except:
        return ""

def run_ai():
    command = take_command()
    print(f"DEBUG: Recognized command: {command}")

    if 'youtube' in command:
        talk("Opening YouTube 🎬")
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in command:
        talk("Opening Google 🌐")
        webbrowser.open("https://www.google.com")

    elif 'play' in command:
        song = command.replace('play', '')
        talk(f'Playing {song} 🎶')
        pywhatkit.playonyt(song)
    
    elif 'git hub' in command:
        talk("Opening GitHub 💻")
        webbrowser.open("https://github.com")

    elif 'instagram' in command:
        talk("Opening Instagram 📸")
        webbrowser.open("https://www.instagram.com")

    else:
        talk("Sorry, i can't understand that command!! kuki aapke mummy ki aawaj aarhi hai ")
        return False  # Stop if not understood

    return True  # Continue if a command was recognized

# Run until an unknown command is given
while True:
    if not run_ai():
        break
