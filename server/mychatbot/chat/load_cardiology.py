import os
import sys
import json

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mychatbot.settings")
django.setup()

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
# LOAD FILE
# -----------------------------
file_path = os.path.join(os.path.dirname(__file__), "cardiology.txt")

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Loaded {len(data)} records")

# -----------------------------
# GET EXISTING IDS (avoid duplicates)
# -----------------------------
cursor.execute("SELECT id FROM cardiology_data")
existing_ids = set([row[0] for row in cursor.fetchall()])

# -----------------------------
# INSERT DATA
# -----------------------------
inserted = 0

for item in data:
    id_ = item["id"]

    # Skip if already exists
    if id_ in existing_ids:
        continue

    topic = item["topic"]
    type_ = item["type"]
    text = item["text"]
    variations = item["variations"]

    #  Use ONLY main text for embedding (better accuracy)
    embedding = model.encode(text).tolist()

    cursor.execute(
        """
        INSERT INTO cardiology_data (id, topic, type, text, variations, embedding)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (id_, topic, type_, text, variations, embedding)
    )

    inserted += 1

# -----------------------------
# COMMIT (VERY IMPORTANT)
# -----------------------------
conn.commit()

print(f"Inserted {inserted} new records successfully!")