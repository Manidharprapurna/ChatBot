from .vector_store import search_vector

# MAIN CHATBOT FUNCTION
def slm_response(user_message: str) -> str:
    if not user_message.strip():
        return "Please type a message."

    try:
        # VECTOR SEARCH
        results = search_vector(user_message)

        if results:
            # Return the best match directly from the vector store
            return results[0].answer

        return "I don't have information about that."

    except Exception as e:
        print(f"[ERROR]: {e}")
        return "Something went wrong."