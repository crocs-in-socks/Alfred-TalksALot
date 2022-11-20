import pyttsx3
import datetime
import wikipedia
import webbrowser
import os

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet():
    hour = int(datetime.datetime.now().hour)
    
    if(hour >= 6 and hour <= 12):
        speak("Good morning sir")
    elif(hour > 12 and hour < 16):
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

def takeCommand():
    said = input()
    return said

def searchWiki(str):
    speak("I'll search that up")
    str = str.replace("wiki", "")

    try:
        search_result = wikipedia.summary(str, sentences=2)
        speak(search_result)
    except:
        other_results = wikipedia.search(str, results=5)
        if(other_results):
            speak("I couldn't quite find that, but this is what I found:")
            for result in other_results:
                speak(result)
                print(result)
        else:
            speak("I couldn't find anything related to that")

# Try to get this to work for firefox
def openSite(url):
    url = url + ".com"
    webbrowser.open(url)

accessible_sites = ["google", "youtube", "stackoverflow"]
accessible_apps = []

if __name__ == "__main__":
    greet()

    while True:
        query = takeCommand().lower()

        if "wiki" in query:
            searchWiki(query)
        
        elif "open" in query:
            openRequest = query.split(" ")
            if openRequest[1] in accessible_sites:
                openSite(openRequest[1])