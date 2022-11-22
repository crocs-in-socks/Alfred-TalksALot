import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import pywhatkit

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

accessible_sites = ["google", "youtube", "stackoverflow"]
accessible_apps = ["spotify", "whatsapp", "notepad", "calculator", "githubdesktop"]
app_routes =   {"spotify" : "C:\\Users\\gouri\\OneDrive\\Desktop\\Spotify.lnk", 
                "whatsapp" : "C:\\Users\\gouri\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
                "notepad" : "C:\\Program Files\\WindowsApps\\Microsoft.WindowsNotepad_11.2209.6.0_x64__8wekyb3d8bbwe\\Notepad\\Notepad.exe",
                "calculator" : "C:\\Windows\\System32\\calc.exe",
                "githubdesktop" : "C:\\Users\\gouri\\AppData\\Local\\GitHubDesktop\\GitHubDesktop.exe"}

def speak(audio):
    """Says the given string"""

    print()
    print("Alfred : " + audio)
    print()
    engine.say(audio)
    engine.runAndWait()

def greet():
    """Greets based on time of day"""

    hour = int(datetime.datetime.now().hour)
    
    if(hour >= 6 and hour <= 12):
        speak("Good morning sir")
    elif(hour > 12 and hour < 16):
        speak("Good afternoon sir")
    else:
        speak("Good evening sir")

def takeCommand():
    """Take an input from user"""

    said = input()
    return said

def searchWiki(str):
    """Searches wikipedia"""

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
        else:
            speak("I couldn't find anything related to that")

def searchInGeneral(topic):
    """Searches google"""

    pywhatkit.search(topic)

def play(video):
    """Plays a video from youtube"""

    pywhatkit.playonyt(video)

# Try to get this to work for firefox
def openSite(url):
    """Opens a website"""

    url = url + ".com"
    webbrowser.open(url)

def openApp(appName):
    """Opens an app using appName and app_route"""

    os.startfile(app_routes[appName])


if __name__ == "__main__":
    greet()

    while True:
        query = takeCommand().lower()

        if "wiki" in query:
            searchWiki(query)
        
        elif "open" in query:
            openRequest = query.split(" ")
            if openRequest[-1] in accessible_sites:
                speak("Sure, just hold on a moment")
                openSite(openRequest[-1])
            elif openRequest[-1] in accessible_apps:
                speak("Sure, just hold on a moment")
                openApp(openRequest[-1])
            else:
                speak("I couldn't quite find anything like that")
        
        elif ("what" in query) or ("how" in query):
            searchInGeneral(query)
        
        elif "play" in query:
            query = query.replace("play ", "")
            play(query)
        
        elif "joke" in query:
            speak(pyjokes.get_joke())

        elif "shutdown" in query:
            speak("Do you want to shutdown the system?")
            confirmation = input()
            if confirmation == "y":
                os.system("shutdown /s /t 1")
        
        elif "thanks" and "alfred" in query:
            speak("Have a nice day!")
            exit()
        
        else:
            speak("I couldn't quite catch that, could you come again?")