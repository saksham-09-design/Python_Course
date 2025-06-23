import speech_recognition as sr
import pyttsx3
import pyautogui
import wikipedia
import google.generativeai as genAi
from gen_AI_Api import *
import requests
import random
import pywhatkit
from datetime import datetime
import string
import os



client = genAi.configure(api_key=apiKey)
model = genAi.GenerativeModel("gemini-1.5-flash")
engine = pyttsx3.init()
urlWeather = "http://api.weatherapi.com/v1/current.json"


quotes = ["Do not wait for the perfect moment, take the moment and make it perfect.",
"Life is what happens when you're busy making other plans. – John Lennon",
"Believe you can and you're halfway there. – Theodore Roosevelt",
"Success is not final, failure is not fatal: It is the courage to continue that counts. – Winston Churchill",
"In the middle of difficulty lies opportunity. – Albert Einstein",
"If you want to lift yourself up, lift up someone else. – Booker T. Washington",
"Happiness is not something ready made. It comes from your own actions. – Dalai Lama",
"What you do today can improve all your tomorrows. – Ralph Marston",
"Don’t watch the clock; do what it does. Keep going. – Sam Levenson",
"The best way to predict the future is to create it. – Peter Drucker",
"You miss 100% of the shots you don't take. – Wayne Gretzky",
"The only limit to our realization of tomorrow is our doubts of today. – Franklin D. Roosevelt",
"Be yourself; everyone else is already taken. – Oscar Wilde",
"Act as if what you do makes a difference. It does. – William James",
"Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart. – Roy T. Bennett",
"Dream big. Start small. Act now. – Robin Sharma",
"It always seems impossible until it’s done. – Nelson Mandela",
"Courage doesn’t always roar. Sometimes it’s the quiet voice at the end of the day saying, ‘I will try again tomorrow.' – Mary Anne Radmacher",
"Do what you can, with what you have, where you are. – Theodore Roosevelt",
"The only way to do great work is to love what you do. – Steve Jobs",
"Simplicity is the ultimate sophistication. – Leonardo da Vinci",
"You only live once, but if you do it right, once is enough. – Mae West",
"Be the change that you wish to see in the world. – Mahatma Gandhi",
"Success usually comes to those who are too busy to be looking for it. – Henry David Thoreau",
"Don’t limit your challenges. Challenge your limits."]

jokes = [
"Why do Python programmers have low self-esteem? Because they’re constantly comparing their self to others.",
"I told my computer I needed a break, and it said no problem—it’ll go to sleep.",
"Why did the programmer quit his job? Because he didn't get arrays.",
"Why do Java developers wear glasses? Because they don’t C#.",
"Why did the developer go broke? Because he used up all his cache.",
"Debugging: Being the detective in a crime movie where you are also the murderer.",
"What's a programmer's favorite hangout place? The Foo Bar.",
"Why did the Python live on land? Because it didn’t like working with sea-lists.",
"How do you comfort a JavaScript bug? You console it.",
"A SQL query walks into a bar, walks up to two tables and says, ‘Can I join you?’",
"Why do programmers prefer dark mode? Because light attracts bugs.",
"Why did the Boolean break up with the Integer? Because they couldn’t agree on anything!",
"How does a computer get drunk? It takes screenshots.",
"Why couldn’t the string become an integer? Because it couldn’t parse itself.",
"What do you call 8 hobbits? A hobbyte.",
"How many programmers does it take to change a light bulb? None. That’s a hardware problem.",
"Why do Python devs hate snakes? Because they can't catch syntax errors in the wild.",
"Why was the function sad? Because it didn’t return anything.",
"I used to play piano by ear, but now I use my hands like a normal person.",
"What’s a computer’s favorite beatle song? 'Let it BINARY!'"
]

pickup_lines = [
"Are you a magician? Because whenever I look at you, everyone else disappears.",
"Do you have a name, or can I call you mine?",
"Are you Wi-Fi? Because I'm feeling a connection.",
"Are you made of copper and tellurium? Because you're Cu-Te.",
"Is your name Google? Because you’ve got everything I’ve been searching for.",
"Do you have a map? I just got lost in your eyes.",
"Are you a keyboard? Because you're just my type.",
"Can I follow you? Because my mom told me to follow my dreams.",
"Is your name Java? Because you’ve got me brewing with love.",
"Do you believe in love at first sight—or should I walk by again?",
"Are you a campfire? Because you're hot and I want s'more.",
"Are you French? Because Eiffel for you.",
"Are you a time traveler? Because I can see you in my future.",
"Are you a cloud? Because you brighten my day.",
"Are you an exception? Because I can’t seem to handle you.",
"Are you an algorithm? Because you sort my heart out.",
"Are you a charger? Because without you, I’d die.",
"If you were a vegetable, you’d be a cute-cumber.",
"Are you an angle? Because you’re acute one.",
"Are you a loop? Because I keep falling for you over and over."
]

rememberThing = ""




def speak(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    inp = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listning....")
        input_aud = inp.listen(source=source)
        try:
            print("Recognising....")
            user_text = inp.recognize_google(input_aud,language="en-in")
            return user_text
        except:
            return "Recognition Failed!"

def search_wikipedia(term):
    try:
        result = wikipedia.summary(term,5)
    except:
        result = "No Data Found on Wikipedia for this Term."
    return result

def gemini_response(prompt):
    try:
        respose = model.generate_content(prompt)
        print(f"Gemini: {respose.text.replace("**","")}")
    except:
        print("An Error Occured!")

def fetch_weather(location):
    params = {
        'key' : weather_API,
        'q' : location
    }
    respose = requests.get(url=urlWeather,params=params)
    if respose.status_code == 200:
        data = respose.json()
        temprature = data['current']['temp_c']
        condition = data['current']['condition']['text']
        wind = data['current']['wind_kph']
        return f"Its {condition} with a temprature of {temprature} degree celcius and a wind speed of {wind} kilo meter per hour."
    else:
        return "Error Fetching Weather Data!"
def play_youtube(tittle):
    pywhatkit.playonyt(tittle)

def game():
    while True:
        print("Press E for Exiting.")
        userChoice = input("Please choose from Rock/Paper/Scissor (R/P/S): ").lower()
        if userChoice == 'e':
            return
        compChoice = random.choice(['r','s','p'])
        print(f"User: {userChoice}")
        print(f"Computer: {compChoice}")
        if userChoice == compChoice:
            print("It's a Tie.")
        if userChoice == 'r' and compChoice == 'p':
            print("Computer Won")
        elif userChoice == 'r' and compChoice == 's':
            print("User Won")
        elif userChoice == 'p' and compChoice == 's':
            print("Comptuer Won")
        elif userChoice == 'p' and compChoice == 'r':
            print("User Won")
        elif userChoice == 's' and compChoice == 'r':
            print("Comptuer Won")
        elif userChoice == 's' and compChoice == 'p':
            print("User Won")
def genPass():
    lowerCase = string.ascii_lowercase
    upperCase = string.ascii_uppercase
    digits = string.digits
    special = "@#$-_.!"
    allChar = lowerCase + upperCase + digits + special
    password = ""
    length = random.randint(8,16)
    for i in range(length+1):
        password += random.choice(allChar)
    print(password)

while True:
    user_Input = take_command()

    if "hello jarvis" in user_Input.lower():
        print("Hello, Welcome back Sir.")
        speak("Hello, Welcome back Sir.")
    if "launch" in user_Input.lower():
        app = user_Input.replace("launch","")
        pyautogui.press('win')
        pyautogui.sleep(0.3)
        pyautogui.typewrite(app)
        pyautogui.sleep(0.3)
        pyautogui.press('enter')
        speak(f"{app} Launched Sir!")
    if "close the window" in user_Input.lower():
        pyautogui.hotkey('alt','f4')
        speak(f"Window Closed Sir!")
    if "change the tab" in user_Input.lower():
        pyautogui.hotkey('alt','tab')
    if "search" in user_Input.lower():
        term = user_Input.replace("search","")
        result = search_wikipedia(term)
        print(result)
        choice = input("Do you want me to speak? Y/N")
        if choice.lower() == "y":
            speak(result)
        else:
            pass
    if "act as chatbot" in user_Input.lower():
        while(True):
            print("Type exit to Return to Audio Mode.")
            userPrompt = input("Enter Prompt: ")
            if userPrompt.lower() == "exit":
                break
            else:
                gemini_response(userPrompt)
    if "weather at" in user_Input.lower():
        loc = user_Input.replace("weather at","").replace("current","")
        result = fetch_weather(loc)
        print(result)
        speak(result)
    if "quote" in user_Input.lower():
        q = random.choice(quotes)
        print(q)
        speak(q)
    if "joke" in user_Input.lower():
        j = random.choice(jokes)
        print(j)
        speak(j)
    if "pickup line" in user_Input.lower():
        q = random.choice(pickup_lines)
        print(q)
        speak(q)
    if "on youtube" in user_Input.lower():
        tittle = user_Input.replace("on youtube","").replace("play","")
        play_youtube(tittle=tittle)
    if "take a note" in user_Input.lower():
        print("Ok, I will save all things you speak.")
        speak("Ok, I will save all things you speak.")
        note = take_command()
        print(f"Note: {note}")
        print("Now give the tittle for the note")
        speak("Now give the tittle for the note")
        tittle = take_command()
        print(f"Tittle: {tittle}")
        with open(f"{tittle}.txt","w") as file:
            file.write(f"{tittle}\n{note}")
        file.close()
        speak(f"Note saved with tittle {tittle}")
    if "what time is it" in user_Input.lower():
        time = datetime.now().strftime("Its %H %M")
        print(time)
        speak(time)
    if "what date is it" in user_Input.lower():
        date = datetime.now().strftime("Its %D of Month %m")
        print(date)
        speak(date)
    if "play a game" in user_Input.lower():
        speak("Ok, Let's play Rock, Paper and scissors")
        print("Ok, Let's play Rock, Paper and scissors")
        game()
    if "password" in user_Input.lower():
        print("Ok, Here is a strong Password: ")
        speak("Ok, Here is a strong Password: ")
        genPass()
    if "increase the brightness" in user_Input.lower():
        os.system('WMIC /NAMESPACE:\\\\root\\wmi PATH WmiMonitorBrightnessMethods WHERE "Active=TRUE" CALL WmiSetBrightness Brightness=100 Timeout=0')
        print("Brightness Increased Sir!")
        speak("Brightness Increased Sir!")
    if "decrease the brightness" in user_Input.lower():
        os.system('WMIC /NAMESPACE:\\\\root\\wmi PATH WmiMonitorBrightnessMethods WHERE "Active=TRUE" CALL WmiSetBrightness Brightness=10 Timeout=0')
        print("Brightness Decreased Sir!")
        speak("Brightness Decreased Sir!")
    if "screenshot" in user_Input.lower():
        screenshot = pyautogui.screenshot()
        screenshot.save(f"D:\\{random.randint(0,999999999999)}.png")
        print("Screenshot Taken Sir!")
        speak("Screenshot Taken Sir!")
    if "volume up" in user_Input.lower():
        for i in range(20):
            pyautogui.press('volumeup')
    if "volume down" in user_Input.lower():
        for i in range(20):
            pyautogui.press('volumedown')
    if "mute" in user_Input.lower():
        pyautogui.press('volumemute')
    if "remember this" in user_Input.lower():
        thingToRemember = user_Input.replace("remember this","")
        rememberThing = thingToRemember
        print("Rememberd sir.")
        speak("Rememberd sir.")
    if "what i asked you to remember" in user_Input.lower():
        print(f"You told {rememberThing} to remember")
        speak(f"You told {rememberThing} to remember")
    if "say hello to" in user_Input.lower():
        personName = user_Input.replace("say hello to","").replace("hey","")
        print(f"Hello {personName}")
        speak(f"Hello {personName}")
    if "exit system" in user_Input.lower():
        print("Exiting system Sir, Have a nice day!")
        speak("Exiting system Sir, Have a nice day!")
        break

