from crate import client
from sentence_transformers import SentenceTransformer

conn = client.connect("http://localhost:4200", username="crate")
cursor = conn.cursor()

model = SentenceTransformer("all-MiniLM-L6-v2")


def search_crate(query, k=3):
    query_embedding = model.encode(query).tolist()

    cursor.execute(
        """
        SELECT text, embedding <-> ? AS score
        FROM cardiology_data
        ORDER BY score ASC
        LIMIT ?
        """,
        (query_embedding, k)
    )

    rows = cursor.fetchall()

    # filter + best result
    if not rows:
        return None

    best_text, best_score = rows[0]

    print("Best score:", best_score)

    # threshold (important)
    if best_score > 1.2:   # smaller is better
        return None

    return best_text