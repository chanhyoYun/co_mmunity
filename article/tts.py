import pyttsx3

def tts(content):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(content)
    engine.runAndWait()
    return True