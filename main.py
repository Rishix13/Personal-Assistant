import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wolframalpha
import requests
import sys
import webbrowser
import bs4

client = wolframalpha.Client('E76QY4-Q9WVKK5Q8K')

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    try:
        with sr.Microphone() as source:
            print("Hello Sir")
            #talk("Hello Sir , How are you ?, I am your personal assistant")
            print('I am listening...')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command = command.replace('jarvis', '')
    except:
        pass
    return command

def run_assistant():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        talk('playing ' + song)
        pywhatkit.playonyt(song)
        print('playing' + song)

    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print(time)
        talk('Current Time is '+time)

    elif 'search' in command:
        value = command.replace('search', '')
        talk('searching ' + value)
        print('searching' + value)
        temp = requests.get('https://google.com/search?p='+value)
        temp.raise_for_status()
        soup = bs4.BeautifulSoup(temp.text, "html.parser")
        linkelements = soup.select('.r a')
        linkstoopen = min(1, len(linkelements))
        for i in range(linkstoopen):
            webbrowser.open('https://google.com'+linkelements[i].get('href'))

    else:
        res = client.query(command)
        ans = next(res.results).text
        print(ans)
        talk(ans)

run_assistant()