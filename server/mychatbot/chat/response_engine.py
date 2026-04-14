import random
import re
from .crate_service import search_cardiology


# -----------------------------
# STEP 1: DETECT QUESTION TYPE
# -----------------------------
def detect_type(query):
    query = query.lower()

    if "symptom" in query:
        return "symptoms"
    elif "treatment" in query or "treat" in query:
        return "treatment"
    elif "prevent" in query:
        return "prevention"
    elif "risk" in query:
        return "risk_factors"
    elif "test" in query or "diagnosis" in query:
        return "diagnosis"
    elif "procedure" in query:
        return "procedures"
    elif "emergency" in query or "heart attack" in query:
        return "emergency"
    else:
        return "definition"


# -----------------------------
# STEP 2: SPLIT SENTENCES
# -----------------------------
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if s.strip()]


# -----------------------------
# STEP 3: VARIATION ENGINE
# -----------------------------
def generate_variation(results):
    all_sentences = []

    for row in results:
        text = row["text"]
        variations = row["variations"] or []

        # Add main text sentences
        all_sentences.extend(split_sentences(text))

        # Add variation sentences
        for v in variations:
            all_sentences.append(v)

    # Remove duplicates
    all_sentences = list(set(all_sentences))

    # Pick random sentences
    selected = random.sample(
        all_sentences,
        min(3, len(all_sentences))
    )

    # Shuffle order
    random.shuffle(selected)

    return " ".join(selected)


# -----------------------------
# STEP 4: SAFETY LAYER
# -----------------------------
def apply_safety(response, query):
    query = query.lower()

    # Emergency detection
    if any(word in query for word in ["chest pain", "heart attack", "collapse"]):
        return "This may be a medical emergency. Please seek immediate medical attention."

    # If empty response
    if not response or len(response.strip()) == 0:
        return "I don't have enough information. Please consult a doctor."

    return response


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def generate_response(user_query):
    # Detect type
    q_type = detect_type(user_query)

    # Get data from DB
    results = search_cardiology(user_query, q_type)

    if not results:
        return "I don't have enough information. Please consult a doctor."

    # Generate variation
    response = generate_variation(results)

    # Apply safety
    response = apply_safety(response, user_query)

    return response