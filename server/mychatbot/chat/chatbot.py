import json
import os
import random
import nltk
from nltk.stem import WordNetLemmatizer

# Download resources (first time only)
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Load intents
# Construct an absolute path to intents.json assuming it is in the same directory as this file
current_dir = os.path.dirname(os.path.abspath(__file__))
intents_path = os.path.join(current_dir, 'intents.json')

with open(intents_path) as file:
    intents = json.load(file)

# Preprocess text
def clean_sentence(sentence):
    words = nltk.word_tokenize(sentence.lower())
    words = [lemmatizer.lemmatize(word) for word in words]
    return words

# Detect intent
def get_intent_tag(sentence):
    sentence_words = clean_sentence(sentence)
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            pattern_words = clean_sentence(pattern)
            if any(word in sentence_words for word in pattern_words):
                return intent['tag']
    return None

# Get bot response
def get_response(sentence):
    tag = get_intent_tag(sentence)
    if tag:
        for intent in intents['intents']:
            if intent['tag'] == tag:
                return random.choice(intent['responses'])
    return "Sorry, I didn't understand that."