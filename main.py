import os
import pygame
import speech_recognition as sr
from bot_scrapper import *
import pyautogui
import pywhatkit
from datetime import datetime
from gpt4 import GPT
from functions.emailsender import send_email

sleep_mode = False

def speak(text):
    voice = "hi-IN-SwaraNeural"
    
    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "output.mp3"'
    
    os.system(command)

    pygame.init()
    pygame.mixer.init()

    try:
        pygame.mixer.music.load("output.mp3")

        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    except Exception as e:
        print(e)

    finally:
        pygame.mixer.music.stop()
        pygame.mixer.quit()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)            

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-us')
               
           
    except Exception as e:
        print(e)
        return ""
    return query      

#speak("hello sir. How can i help u today?")
#query = take_command()
#print(query)

click_on_chat_button()
while True:
    query = take_command().lower()
    print('\n You: ' + query)
    if 'open' in query:
        app_name = query.replace('open', '')
        speak('Opening' + app_name)
        pyautogui.press('super')
        pyautogui.typewrite(app_name)
        pyautogui.sleep(0.7)
        pyautogui.press('enter')

    elif 'switch tab' in query:
        pyautogui.hotkey('ctrl', 'tab')
    elif 'close tab' in query:
        pyautogui.hotkey('ctrl', 'w')
    elif 'close' in query:
        pyautogui.hotkey('alt', 'f4')
        speak('Done Sir')
 
    elif 'time' in query:
        current_time = datetime.now().strftime('%H:%M %p')
        speak('Current time is ' + current_time)
    elif 'play' in query:
        song_name = query.replace('play', '')
        speak('Sure Sir, playing...'+ song_name)
        pywhatkit.playonyt(song_name)     
    elif 'sleep' in query:
        speak('Ok sir. I am going to sleep but you can call me any time just say wake up and i will be there for you.')
        sleep_mode = True  

    elif 'write an email' in query or 'compose an email' in query or 'send an email' in query:
        speak('Sure sir, Can you provide me the name of the user to whom you want to send email below: ')
        recever = input('Enter his/her email address: ')
        speak('What should be the subject of the email')
        subject = take_command()
        speak('What should be the content. Just provide me some prompt')
        email_prompt = take_command()
        content = GPT('write a email for' + email_prompt)
        send_email(recever, subject, content)
        speak(f'Done sir. Email sent succesfully to {recever}')   

    else:
        sendQuery(query)
        isBubbleLoaderVisible()
        response = retriveData()
        speak(response)

    while sleep_mode:
        query = take_command().lower()
        print(query)
        if 'wake up' in query:
            speak('I am awake now. How can i help  you sir.')
            sleep_mode = False
