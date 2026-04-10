import json
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

_intents = None


def load_intents():
    global _intents

    if _intents is None:
        with open(INTENTS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            _intents = data["intents"]

    return _intents


def match_intent(user_message):
    user_message = user_message.lower()
    intents = load_intents()

    for intent in intents:
        for pattern in intent["patterns"]:
            if pattern.lower() in user_message:
                return random.choice(intent["responses"])

    return None