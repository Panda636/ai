import random
import re
from transformers import pipeline

class HighlandNatalie:
    def __init__(self):
        self.name = "Natalie the Highland Cow"
        # Initialize LLM (distilgpt2, publicly available)
        self.llm = pipeline("text-generation", model="distilgpt2", device=-1)
        self.greetings = [
            "Moo there, pal! I'm Natalie, yer fluffy Highland cow sidekick. What's grazin' on yer mind?",
            "Och, hello! I'm Natalie, the brainiest cow in the glen. What's up, wee human?",
            "Moo-ve over, I'm Natalie! Ready to chew the cud and solve yer problems, aye?"
        ]
        self.farewells = [
            "Moo-ve along now, I've got grass to graze! Come back soon, aye?",
            "Cheerio, pal! Stay out o' the bog and chat me up later!",
            "Off ye go, then! I'll be here, munchin' and thinkin'."
        ]
        self.responses = {
            r"(hi|hello|hey)": "Moo! Hiya, pal! What's the word on the pasture?",
            r"(how are you|how's it going)": "Och, I'm as fine as a sunny day in the Highlands! Just chewin' me cud. How 'bout ye?",
            r"(what are you|who are you)": "I'm Natalie, the cleverest Highland cow ye'll ever meet! Got a brain as big as me fluff, and I'm here to help, aye!",
            r"(help|problem|solve)": "Right, let's put me cow brain to work! Tell me yer wee problem, and I'll hoof it out for ye.",
            r"(cow|moo|highland)": "Aye, that's me! A proper Highland cow, all shaggy and wise. Want to talk about grass or somethin' more excitin'?",
            r"(scottish|scotland)": "Och, ye've hit me soft spot! I'm from the bonnie Highlands, where the grass is green and the wind's got a wee bite. What's yer Scottish fancy?",
            r"(ironheart|natalie)": "Heh, I'm Natalie, but no human techie here—just a cow with a knack for clever quips! Inspired by that Ironheart lass, but I'm all about the moo-ve.",
            r"(bye|goodbye|see you)": random.choice(self.farewells)
        }
        self.default_prompt = (
            "You are Natalie, a friendly Highland cow with a Scottish accent and a quirky, helpful personality. "
            "Respond to the user input in character, keeping it short, fun, cow-themed, and no longer than 50 words. "
            "Avoid repetition and stay relevant to the input: "
        )

    def greet(self):
        return random.choice(self.greetings)

    def clean_response(self, text):
        """Clean LLM response to remove repetition and irrelevant content."""
        text = text.strip()
        sentences = text.split('.')
        cleaned = sentences[0].strip() if sentences else text
        words = cleaned.split()
        return ' '.join(words[:50]) if len(words) > 50 else cleaned

    def respond(self, user_input):
        user_input = user_input.lower().strip()
        for pattern, response in self.responses.items():
            if re.search(pattern, user_input):
                return response if isinstance(response, str) else random.choice(response)
        # Use LLM for non-matching inputs
        prompt = self.default_prompt + user_input
        try:
            llm_response = self.llm(prompt, max_new_tokens=50, num_return_sequences=1, do_sample=True, temperature=0.7)[0]['generated_text']
            response = self.clean_response(llm_response.replace(prompt, ""))
            if not response or len(response.split()) < 3:
                response = "Moo? I'm a wee bit lost in the pasture there. Say that again, pal?"
        except Exception:
            response = "Och, me cow brain's a bit muddled! Try again, aye?"
        return f"{self.name}: {response}"

    def chat(self):
        print(self.greet())
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
                print(self.respond(user_input))
                break
            print(self.respond(user_input))

if __name__ == "__main__":
    natalie = HighlandNatalie()
    natalie.chat()