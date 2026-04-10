from crate import client
from sentence_transformers import SentenceTransformer
import numpy as np

# -----------------------------
# CONNECTION
# -----------------------------
conn = client.connect("http://localhost:4200", username="crate")
cursor = conn.cursor()

# -----------------------------
# LOAD MODEL
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# COSINE SIMILARITY
# -----------------------------
def cosine_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# --------------------------------------------------
# 1. SEARCH cardiology_data (VECTOR / EMBEDDING)
# --------------------------------------------------
def search_cardiology(query):
    query_embedding = model.encode(query).tolist()

    cursor.execute("SELECT text, embedding FROM cardiology_data")
    rows = cursor.fetchall()

    best_result = None
    best_score = -1

    for text, emb in rows:
        if not text or not emb:
            continue

        emb = np.array(emb)
        score = cosine_sim(query_embedding, emb)

        if score > best_score:
            best_score = score
            best_result = text

    print("Cardiology best score:", best_score)

    # threshold
    if best_score < 0.3:
        return None

    return best_result


# --------------------------------------------------
# 2. SEARCH chat_logs (FAQ / KEYWORD MATCH)
# --------------------------------------------------
def search_chat_logs(query):
    query = query.lower()

    cursor.execute("SELECT message, response FROM chat_logs")
    rows = cursor.fetchall()

    best_match = None
    best_score = 0

    for message, response in rows:
        if not message or not response:
            continue

        message_lower = message.lower()

        #keyword scoring
        score = sum(1 for word in query.split() if word in message_lower)

        if score > best_score:
            best_score = score
            best_match = response

    print("ChatLogs best score:", best_score)

    # threshold
    if best_score < 2:
        return None

    return best_match