import random
import re

class HighlandNatalie:
    def __init__(self):
        self.name = "Natalie the Highland Cow"
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
        self.default_response = [
            "Moo? I'm a wee bit lost in the pasture there. Say that again, pal?",
            "Och, my cow brain's grazin'. Can ye make it clearer for old Natalie?",
            "Hmmm, that's a tough one for a cow to chew on. Got another question?"
        ]

    def greet(self):
        return random.choice(self.greetings)

    def respond(self, user_input):
        user_input = user_input.lower().strip()
        for pattern, response in self.responses.items():
            if re.search(pattern, user_input):
                return response if isinstance(response, str) else random.choice(response)
        return random.choice(self.default_response)

    def chat(self):
        print(self.greet())
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["bye", "goodbye", "exit", "quit"]:
                print(self.respond(user_input))
                break
            print(f"{self.name}: {self.respond(user_input)}")

if __name__ == "__main__":
    natalie = HighlandNatalie()
    natalie.chat()