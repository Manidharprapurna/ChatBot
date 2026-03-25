import torch
from transformers import pipeline
from .models import FAQ

# Using a very capable, lightweight Small Language Model (0.5 Billion parameters)
MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

# Global variable to keep the model in memory after the first load
_slm_pipeline = None

def get_pipeline():
    global _slm_pipeline
    if _slm_pipeline is None:
        print(f"[SLM] Loading local model '{MODEL_ID}' into memory. This may take a minute...")
        _slm_pipeline = pipeline(
            "text-generation",
            model=MODEL_ID,
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto",  # Automatically uses GPU if available, else CPU
        )
        print("[SLM] Local model loaded successfully.")
    return _slm_pipeline

def get_trained_data_context() -> str:
    """Fetch active FAQs from the database to use as the model's knowledge base."""
    try:
        faqs = FAQ.objects.filter(is_active=True)
        if not faqs.exists():
            return "No specific local data available."
        
        context = "Here is the local knowledge base of Frequently Asked Questions:\n"
        for faq in faqs:
            context += f"Q: {faq.question}\nA: {faq.answer}\n\n"
        return context
    except Exception:
        return ""

def slm_response(user_message: str) -> str:
    if not user_message.strip():
        return "Please type a message so I can help you."

    try:
        # 1. Initialize/Get the local model
        slm = get_pipeline()

        # 2. Fetch your trained/database data
        local_context = get_trained_data_context()

        # 3. Construct the prompt with RAG (Retrieval-Augmented Generation)
        system_prompt = (
            "You are a helpful customer support assistant for a company. "
            "Always use the following knowledge base to answer the user's question. "
            "If the answer is not in the knowledge base, do your best to help politely. "
            "Keep your answer concise and friendly.\n\n"
            f"{local_context}"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ]

        # 4. Generate the response locally
        outputs = slm(
            messages,
            max_new_tokens=150,
            temperature=0.3, # Low temperature ensures it sticks strictly to your FAQ facts
            top_p=0.9,
            do_sample=True,
        )
        
        # Extract the assistant's generated text
        generated_text = outputs[0]["generated_text"][-1]["content"]
        return generated_text.strip()

    except Exception as e:
        print(f"[SLM] Unexpected error: {e}")
        return "I'm having trouble accessing my local brain right now. Please try again later."