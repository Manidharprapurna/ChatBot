from crate import client
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONNECT TO CRATEDB
# -----------------------------
conn = client.connect("http://localhost:4200", username="crate")
cursor = conn.cursor()

# -----------------------------
# LOAD MODEL
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# KNN SEARCH
# -----------------------------
def search_cardiology(query, k=5):
    query_embedding = model.encode(query).tolist()

    cursor.execute(
        """
        SELECT text, variations, embedding <-> ? AS score
        FROM cardiology_data
        ORDER BY score ASC
        LIMIT ?
        """,
        (query_embedding, k)
    )

    rows = cursor.fetchall()

    results = []

    for row in rows:
        text = row[0]
        variations = row[1]
        score = row[2]

        # FILTER BAD MATCHES
        if score > 1.2:
            continue

        results.append({
            "text": text,
            "variations": variations,
            "score": score
        })

    return results