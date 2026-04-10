from .vector_store import search_vector
from .intents_handler import match_intent
from .crate_service import search_cardiology, search_chat_logs


def get_response(user_message: str):

    
    # VALIDATION
    
    if not user_message or not user_message.strip():
        return {
            "response": "Please type a message.",
            "source": "none"
        }

    try:
        print("\nUser:", user_message)

        
        # STEP 1: INTENT MATCHING
        
        intent_response = match_intent(user_message)

        if intent_response:
            print("✔ Intent matched")
            return {
                "response": intent_response,
                "source": "Intent"
            }

        
        # STEP 2: GET BOTH RESULTS

        cardio_result = search_cardiology(user_message)
        chat_result = search_chat_logs(user_message)

        print("Cardiology:", cardio_result)
        print("ChatLogs:", chat_result)


        # STEP 3: PRIORITY LOGIC
        
        if cardio_result and chat_result:
            
            # choose longer/more informative answer
            if len(cardio_result) > len(chat_result):
                return {
                    "response": cardio_result,
                    "source": "CrateDB"
                }
            else:
                return {
                    "response": chat_result,
                    "source": "ChatLogs"
                }

        if cardio_result:
            return {
                "response": cardio_result,
                "source": "CrateDB"
            }

        if chat_result:
            return {
                "response": chat_result,
                "source": "ChatLogs"
            }

    
        # STEP 4: VECTOR DB (FALLBACK)
        
        results = search_vector(user_message, k=3)

        if results:
            faq, score = results[0]

            print("Vector score:", score)

            if score > 0.7:
                return {
                    "response": faq.answer,
                    "source": "VectorDB"
                }

        
        # STEP 5: FINAL FALLBACK
        
        return {
            "response": "I don't have information about that.",
            "source": "fallback"
        }

    except Exception as e:
        print("[ERROR]:", str(e))

        return {
            "response": str(e),
            "source": "error"
        }