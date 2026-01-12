import tkinter as tk
from datetime import datetime
import pyttsx3
import requests

# ---------------- CONFIG ----------------
WEATHER_API_KEY = "YOUR API"
DEFAULT_CITY = "Mumbai"

# ---------------- VOICE ----------------
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # female
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# ---------------- MEMORY ----------------
reminders = []

# ---------------- UTILITIES ----------------
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={DEFAULT_CITY}&appid={WEATHER_API_KEY}&units=metric"
        data = requests.get(url).json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"🌤 {DEFAULT_CITY}: {temp}°C, {desc}"
    except:
        return "⚠️ Weather service not available."

def get_location(place):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
        res = requests.get(url, headers={"User-Agent": "SmileyAI"}).json()
        if not res:
            return "Location not found 😕"
        return f"📍 {place}: Latitude {res[0]['lat']}, Longitude {res[0]['lon']}"
    except:
        return "Location error."

def get_date():
    return f"📅 Today's date is {datetime.now().strftime('%d %B %Y')}"

def tell_joke():
    jokes = [
        "😂 Why did the computer catch a cold? Because it forgot to close its Windows!",
        "🤣 Why do programmers love dark mode? Because light attracts bugs!",
        "😄 Why was the math book sad? Too many problems."
    ]
    return jokes[datetime.now().second % len(jokes)]

# ---------------- AI BRAIN ----------------
def get_response(text):
    text = text.lower()

    if "hi" in text or "hello" in text:
        return "Hello 😊 I am Smiley! How can I help you?"

    if "your name" in text:
        return "My name is Smiley 😊"

    if "who do you work for" in text or "whom do you work for" in text:
        return "I work for Dia 💙"

    if "time" in text:
        return f"⏰ Current time is {datetime.now().strftime('%I:%M %p')}"

    if "date" in text or "today" in text:
        return get_date()

    if "weather" in text:
        return get_weather()

    if "where is" in text:
        place = text.replace("where is", "").strip().title()
        return get_location(place)

    if "remind me" in text:
        reminder = text.replace("remind me", "").strip()
        reminders.append(reminder)
        return f"🔔 Reminder added: {reminder}"

    if "show reminders" in text or "my reminders" in text:
        if not reminders:
            return "You have no reminders 😊"
        return "🔔 Your reminders:\n" + "\n".join(reminders)

    if "calendar" in text or "events" in text:
        if not reminders:
            return "📅 No upcoming events."
        return "📅 Upcoming events:\n" + "\n".join(reminders)

    if "joke" in text:
        return tell_joke()

    if "bye" in text:
        return "Goodbye 👋 Take care!"

    return "😊 I'm listening… tell me more."

# ---------------- SEND MESSAGE ----------------
def send_message():
    user_text = entry.get().strip()
    if not user_text:
        return

    chat.config(state="normal")
    chat.insert("end", f"You: {user_text}\n")
    chat.config(state="disabled")
    chat.see("end")
    entry.delete(0, "end")

    reply = get_response(user_text)

    chat.config(state="normal")
    chat.insert("end", f"😊 Smiley: {reply}\n\n")
    chat.config(state="disabled")
    chat.see("end")

    speak(reply)

# ---------------- GUI ----------------
root = tk.Tk()
root.title("Smiley AI 😊")
root.geometry("850x520")
root.configure(bg="#121212")

chat = tk.Text(
    root,
    bg="#1e1e1e",
    fg="white",
    font=("Segoe UI", 11),
    state="disabled",
    wrap="word"
)
chat.pack(expand=True, fill="both", padx=10, pady=10)

chat.config(state="normal")
chat.insert("end", "😊 Smiley: Hello! I am Dia's AI assistant 💙\n\n")
chat.config(state="disabled")

bottom = tk.Frame(root, bg="#121212")
bottom.pack(fill="x", padx=10, pady=10)

entry = tk.Entry(
    bottom,
    font=("Segoe UI", 12),
    bg="#2b2b2b",
    fg="white",
    insertbackground="white"
)
entry.pack(side="left", expand=True, fill="x", padx=(0, 10))
entry.bind("<Return>", lambda e: send_message())

send_btn = tk.Button(
    bottom,
    text="Send 😊",
    command=send_message,
    bg="#333333",
    fg="white",
    font=("Segoe UI", 11),
    width=10
)
send_btn.pack(side="right")

root.mainloop()
