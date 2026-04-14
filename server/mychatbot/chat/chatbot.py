from .vector_store import search_vector
from .intents_handler import match_intent
from .crate_service import search_cardiology
import random


# -----------------------------
# CLEAN TEXT
# -----------------------------
def clean_text(text):
    return text.strip() if text else ""


# -----------------------------
# RESPONSE GENERATOR
# -----------------------------
def generate_variation(context_list):

    if not context_list:
        return ""

    main_text = context_list[0]

    variations = context_list[1:]

    alt = ""
    if variations:
        alt = random.choice(variations)

    templates = [
        main_text,
        alt,
        f"{main_text} {alt}",
        f"In simple terms, {main_text}",
        f"{alt} This is important for heart health.",
        f"{main_text} Doctors use this in diagnosis and treatment."
    ]

    # Remove empty templates
    templates = [t for t in templates if t.strip()]

    return random.choice(templates)


# -----------------------------
# SAFETY LAYER
# -----------------------------
def apply_safety(response, query):
    query = query.lower()

    emergency_words = [
        "chest pain", "heart attack", "collapse",
        "severe pain", "breathing difficulty"
    ]

    if any(word in query for word in emergency_words):
        return "This may be a medical emergency. Please seek immediate medical attention."

    if not response.strip():
        return "I don't have enough information. Please consult a doctor."

    return response


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def get_response(user_message: str):

    if not user_message or not user_message.strip():
        return {
            "response": "Please type a message.",
            "source": "none"
        }

    try:
        print("\nUser:", user_message)

        # -----------------------------
        # STEP 1: INTENT
        # -----------------------------
        intent_response = match_intent(user_message)

        if intent_response:
            return {
                "response": intent_response,
                "source": "Intent"
            }

        # -----------------------------
        # STEP 2: SMART KNN
        # -----------------------------
        cardio_result = search_cardiology(user_message)

        context_list = []

        if cardio_result:
            # 🔥 Take TOP 3 results
            top_results = cardio_result[:3]

            # Random main selection
            main_item = random.choice(top_results)

            context_list.append(clean_text(main_item["text"]))

            if main_item.get("variations"):
                context_list.extend([
                    clean_text(v) for v in main_item["variations"]
                ])

            # Add supporting info
            others = [item for item in top_results if item != main_item]

            if others:
                support_item = random.choice(others)
                context_list.append(clean_text(support_item["text"]))

        # Remove duplicates
        context_list = list(set([c for c in context_list if c]))

        # -----------------------------
        # STEP 3: GENERATE RESPONSE
        # -----------------------------
        if context_list:
            response = generate_variation(context_list)

            response = apply_safety(response, user_message)

            return {
                "response": response,
                "source": "CrateDB + Smart KNN + Variation"
            }

        # -----------------------------
        # STEP 4: VECTOR FALLBACK
        # -----------------------------
        results = search_vector(user_message, k=3)

        if results:
            faq, score = results[0]

            if score > 0.7:
                return {
                    "response": faq.answer,
                    "source": "VectorDB"
                }

        # -----------------------------
        # FINAL FALLBACK
        # -----------------------------
        return {
            "response": "I don't have enough information. Please consult a doctor.",
            "source": "fallback"
        }

    except Exception as e:
        print("[ERROR]:", str(e))

        return {
            "response": str(e),
            "source": "error"
        }