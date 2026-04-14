import requests
import os

API_KEY = os.getenv("OPENROUTER_API_KEY")


def generate_response(query, context_list):
    context_text = "\n".join(context_list)

    print("DEBUG API KEY:", API_KEY)

    if not API_KEY:
        return "API Key is missing. Check .env file."

    prompt = f"""
You are a medical assistant chatbot.

Strict rules:
- Answer ONLY using the context
- Do NOT include unrelated information
- If not found, say: "Please consult a doctor"
- Keep answer clear and professional

Context:
{context_text}

Question:
{query}
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()
    print("API RESPONSE:", data)

    if "choices" in data:
        return data["choices"][0]["message"]["content"]

    if "error" in data:
        return f"API Error: {data['error']['message']}"

    return "Unexpected error"