"""
Voice + Text Chatbot — FREE VERSION (No API key needed)
Uses: pyttsx3 (speech), SpeechRecognition (mic), + smart rule-based AI
"""

import datetime
import os
import random
import json
import urllib.request
import urllib.parse
import speech_recognition as sr
import pyttsx3

# ── TTS ENGINE SETUP ──────────────────────────────────────────────────
engine = pyttsx3.init()
engine.setProperty('rate', 165)
engine.setProperty('volume', 1.0)

# Optional: set a female voice if available
voices = engine.getProperty('voices')
if len(voices) > 1:
    engine.setProperty('voice', voices[1].id)

# ── SPEECH RECOGNIZER ─────────────────────────────────────────────────
recognizer = sr.Recognizer()

# ── LOG FILE ──────────────────────────────────────────────────────────
LOG_FILE = "conversation_log.txt"

def log_message(speaker, message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {speaker}: {message}\n")

# ── SPEAK + PRINT ─────────────────────────────────────────────────────
def speak(text):
    print(f"\n🤖 Bot: {text}")
    log_message("Bot", text)
    engine.say(text)
    engine.runAndWait()

# ── MICROPHONE INPUT ──────────────────────────────────────────────────
def listen_from_mic():
    with sr.Microphone() as source:
        print("\n🎤 Listening... speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio)
        print(f"🧑 You (voice): {text}")
        log_message("You (voice)", text)
        return text
    except sr.UnknownValueError:
        speak("Sorry, I couldn't catch that. Try again?")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable. Please type instead.")
        return ""

# ── FREE AI USING WTTR / WIKIPEDIA APIs ───────────────────────────────
def get_weather(city="your city"):
    try:
        url = f"https://wttr.in/{urllib.parse.quote(city)}?format=3"
        with urllib.request.urlopen(url, timeout=4) as r:
            return r.read().decode("utf-8").strip()
    except:
        return f"Couldn't fetch weather for {city} right now."

def get_wikipedia_summary(query):
    try:
        search_url = (
            "https://en.wikipedia.org/api/rest_v1/page/summary/"
            + urllib.parse.quote(query.replace(" ", "_"))
        )
        with urllib.request.urlopen(search_url, timeout=5) as r:
            data = json.loads(r.read().decode("utf-8"))
            return data.get("extract", "")[:300] + "..."
    except:
        return None

# ── JOKES & FACTS ─────────────────────────────────────────────────────
JOKES = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
    "Why did the developer go broke? He used up all his cache!",
    "A SQL query walks into a bar, walks up to two tables and asks... Can I join you?",
]

FACTS = [
    "Honey never spoils. Archaeologists found 3000-year-old honey in Egyptian tombs!",
    "Octopuses have three hearts and blue blood.",
    "A group of flamingos is called a flamboyance.",
    "Bananas are berries, but strawberries are not.",
    "The Eiffel Tower grows 15 cm taller in summer due to heat expansion.",
]

GREETINGS = ["hi", "hello", "hey", "hii", "good morning", "good evening", "what's up", "sup"]
FAREWELLS = ["bye", "exit", "quit", "goodbye", "see you", "later", "stop"]
THANKS    = ["thanks", "thank you", "thx", "ty", "thankyou"]

# ── SMART RESPONSE ENGINE ─────────────────────────────────────────────
def get_response(user_input):
    text = user_input.lower().strip()

    if not text:
        return "I didn't catch that. Could you say it again?"

    # Greetings
    if any(w in text for w in GREETINGS):
        hour = datetime.datetime.now().hour
        if hour < 12:
            return "Good morning! How can I help you today? 😊"
        elif hour < 17:
            return "Good afternoon! What can I do for you?"
        else:
            return "Good evening! How can I help?"

    # Farewells
    if any(w in text for w in FAREWELLS):
        return "Goodbye! It was great talking to you. Have an amazing day! 👋"

    # Thanks
    if any(w in text for w in THANKS):
        return "You're most welcome! Is there anything else I can help with?"

    # Time
    if "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    # Date
    if "date" in text or "today" in text:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}."

    # Joke
    if "joke" in text:
        return random.choice(JOKES)

    # Fact
    if "fact" in text:
        return random.choice(FACTS)

    # Weather
    if "weather" in text:
        words = text.replace("weather", "").replace("in", "").strip()
        city = words if words else "Trivandrum"
        return get_weather(city)

    # Name
    if "your name" in text or "who are you" in text:
        return "I'm Aria, your personal AI voice assistant! Built with Python and lots of love. 💙"

    # Creator
    if "who made you" in text or "who created you" in text or "who built you" in text:
        return "I was built by a talented developer for this hackathon. Pretty cool, right?"

    # How are you
    if "how are you" in text:
        return "I'm doing great, thanks for asking! Ready to help you with anything. 😄"

    # Capabilities
    if "what can you do" in text or "help" in text:
        return ("I can chat with you, tell jokes, share facts, check the weather, "
                "tell the time and date, and answer general questions using Wikipedia!")

    # Wikipedia fallback for general knowledge
    summary = get_wikipedia_summary(user_input)
    if summary and len(summary) > 50:
        return f"Here's what I found: {summary}"

    # Final fallback
    fallbacks = [
        "That's an interesting question! I'm still learning, but I'll get better.",
        "Hmm, I don't have an answer for that yet. Try asking me something else!",
        "I'm not sure about that one. Want to hear a joke instead?",
        "Great question! My knowledge is growing every day. Ask me something else!",
    ]
    return random.choice(fallbacks)


# ── MAIN LOOP ─────────────────────────────────────────────────────────
def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 55)
    print("       🤖  ARIA — Voice & Text AI Assistant")
    print("=" * 55)
    print("  Type your message  OR  type 'voice' to speak")
    print("  Type 'bye' to exit")
    print("=" * 55)

    log_message("System", "=== New conversation started ===")
    speak("Hello! I'm Aria, your AI assistant. How can I help you today?")

    while True:
        try:
            user_in = input("\n💬 You: ").strip()
        except (KeyboardInterrupt, EOFError):
            speak("Goodbye!")
            break

        if user_in.lower() == "voice":
            user_in = listen_from_mic()
            if not user_in:
                continue
        else:
            log_message("You", user_in)

        if not user_in:
            continue

        response = get_response(user_in)
        speak(response)

        if any(w in user_in.lower() for w in FAREWELLS):
            break

    log_message("System", "=== Conversation ended ===")
    print(f"\n📁 Conversation saved to: {os.path.abspath(LOG_FILE)}")


if __name__ == "__main__":
    main()