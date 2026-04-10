import os
import sys
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mychatbot.settings")
django.setup()

from sentence_transformers import SentenceTransformer
from crate import client

# Connect to CrateDB
conn = client.connect("http://localhost:4200", username="crate")
cursor = conn.cursor()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# READ FILE
file_path = os.path.join(os.path.dirname(__file__), "cardiology.txt")

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# SPLIT TEXT (VERY IMPORTANT)
raw_chunks = re.split(r'\.\s+|\n+', text)

print("Raw chunks:", len(raw_chunks))

# CLEAN DATA
clean_chunks = []
seen = set()

for chunk in raw_chunks:
    chunk = chunk.strip()

    if len(chunk) < 50:
        continue

    if chunk in seen:
        continue

    seen.add(chunk)
    clean_chunks.append(chunk)

print("Clean chunks:", len(clean_chunks))

# INSERT INTO DB
for i, chunk in enumerate(clean_chunks):
    chunk = chunk.strip()

    # REMOVE JSON FORMAT IF PRESENT
    if chunk.startswith('"text":'):
        chunk = chunk.replace('"text":', '').strip()

    # remove extra quotes
    chunk = chunk.strip('"')

    # optional: remove leading/trailing commas or braces
    chunk = chunk.strip(",{} ")

    embedding = [float(x) for x in model.encode(chunk)]

    cursor.execute(
        "INSERT INTO cardiology_data (id, text, embedding) VALUES (?, ?, ?)",
        (i, chunk, embedding)
    )

print("Data inserted successfully!")