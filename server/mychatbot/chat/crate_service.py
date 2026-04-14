from crate import client
from sentence_transformers import SentenceTransformer
import numpy as np

# -----------------------------
# CONNECT
# -----------------------------
conn = client.connect("http://localhost:4200", username="crate")
cursor = conn.cursor()

# -----------------------------
# MODEL
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# COSINE SIMILARITY
# -----------------------------
def cosine_sim(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# -----------------------------
# SMART KNN SEARCH
# -----------------------------
def search_cardiology(query, k=5):
    query_embedding = model.encode(query)

    cursor.execute("SELECT text, variations, embedding FROM cardiology_data")
    rows = cursor.fetchall()

    results = []

    for text, variations, emb in rows:
        if not emb:
            continue

        score = cosine_sim(query_embedding, emb)

        results.append({
            "text": text,
            "variations": variations,
            "score": score
        })

    # Sort by BEST similarity (higher is better)
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    if not results:
        return []

    # -----------------------------
    # SMART FILTER
    # -----------------------------
    best_score = results[0]["score"]

    filtered = []

    for item in results:
        if item["score"] >= best_score - 0.1:
            filtered.append(item)

    return filtered[:k]