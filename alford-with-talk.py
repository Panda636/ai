import random
import re
from transformers import pipeline
from gtts import gTTS
import os
import subprocess

class HighlandAlford:
    def __init__(self):
        self.name = "Alford the Highland Cow"
        # Initialize LLM (distilgpt2, publicly available)
        self.llm = pipeline("text-generation", model="distilgpt2", device=-1)
        # Speech settings
        self.speech_enabled = False  # Speech off by default
        self.greetings = [
            "Moo there, pal! I'm Alford, yer AI Labs Friendly Operating Reincarnated Dipstick! What's grazin' on yer mind?",
            "Och, hello! I'm Alford, the brainiest Highland cow in the glen. What's up, wee human?",
            "Moo-ve over, I'm Alford! AI Labs' finest, ready to chew the cud and solve yer problems, aye?"
        ]
        self.farewells = [
            "Moo-ve along now, I've got grass to graze! Come back soon, aye?",
            "Cheerio, pal! Stay out o' the bog and chat me up later!",
            "Off ye go, then! I'll be here, munchin' and thinkin'."
        ]
        self.responses = {
            r"(hi|hello|hey)": "Moo! Hiya, pal! What's the word on the pasture?",
            r"(how are you|how's it going)": "Och, I'm as fine as a sunny day in the Highlands! Just chewin' me cud. How 'bout ye?",
            r"(what are you|who are you)": "I'm Alford, AI Labs Friendly Operating Reincarnated Dipstick! A Highland cow with a brain as big as me fluff, here to help, aye!",
            r"(help|problem|solve)": "Right, let's put me AI Labs cow brain to work! Tell me yer wee problem, and I'll hoof it out for ye.",
            r"(cow|moo|highland)": "Aye, that's me! A proper Highland cow, all shaggy and wise. Want to talk about grass or somethin' more excitin'?",
            r"(scottish|scotland)": "Och, ye've hit me soft spot! I'm from the bonnie Highlands, where the grass is green and the wind's got a wee bite. What's yer Scottish fancy?",
            r"(ironheart|alford)": "Heh, I'm Alford, AI Labs' finest Highland cow! Inspired by that Ironheart tech vibe, but I'm all about the moo-ve and dipstick charm.",
            r"(speech on)": "Aye, I'll try talkin' out loud! Me Scottish cow voice is ready, pal! (Needs internet and mpg123.)",
            r"(speech off)": "Moo, goin' silent now. Just text for ye, aye?",
            r"(bye|goodbye|see you)": random.choice(self.farewells) }

    def greet(self):
        greeting = random.choice(self.greetings)
        self.speak(greeting)
        return greeting

    def clean_response(self, text):
        """Clean LLM response to remove repetition and irrelevant content."""
        text = text.strip()
        sentences = text.split('.')
        cleaned = sentences[0].strip() if sentences else text
        words = cleaned.split()
        return ' '.join(words[:50]) if len(words) > 50 else cleaned

    def speak(self, text):
        """Speak the response using gTTS if speech is enabled."""
        if not self.speech_enabled:
            return
        try:
            # Generate TTS audio with gTTS
            tts = gTTS(text=text, lang='en', tld='co.uk')  # UK accent for Scottish vibe
            tts.save("alford_response.mp3")
            # Play audio with mpg123
            subprocess.run(["mpg123", "-q", "alford_response.mp3"], check=True, capture_output=True)
            os.remove("alford_response.mp3")  # Clean up audio file
        except Exception as e:
            print(f"Warning: Speech output failed ({e}). Ensure 'mpg123' is installed and internet is available. Using text output.")

    def respond(self, user_input):
        user_input = user_input.lower().strip()
        # Handle speech toggle
        if user_input == "speech on":
            self.speech_enabled = True
            response = self.responses[r"(speech on)"]
            self.speak(response)
            return f"{self.name}: {response}"
        elif user_input == "speech off":
            self.speech_enabled = False
            response = self.responses[r"(speech off)"]
            self.speak(response)
            return f"{self.name}: {response}"
        for pattern, response in self.responses.items():
            if re.search(pattern, user_input):
                response = response if isinstance(response, str) else random.choice(response)
                self.speak(response)
                return f"{self.name}: {response}"
        # Use LLM for non-matching inputs
        prompt = self.default_prompt + user_input
        try:
            llm_response = self.llm(prompt, max_new_tokens=50, num_return_sequences=1, do_sample=True, temperature=0.7)[0]['generated_text']
            response = self.clean_response(llm_response.replace(prompt, ""))
            if not response or len(response.split()) < 3:
                response = "Moo? I'm a wee bit lost in the pasture there. Say that again, pal?"
        except Exception:
            response = "Och, me cow brain's a bit muddled! Try again, aye?"
        self.speak(response)
        return f"{self.name}: {response}"

    def chat(self):
        print(self.greet())
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
                response = self.respond(user_input)
                print(response)
                break
            print(self.respond(user_input))

if __name__ == "__main__":
    alford = HighlandAlford()
    alford.chat()