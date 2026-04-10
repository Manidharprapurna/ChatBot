import json
import psycopg2
import uuid

# Load JSON
with open("chat/intents.json") as f:
    data = json.load(f)

# Connect CrateDB
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="crate",
    password="",
    database="doc"
)
cur = conn.cursor()

# Insert data
for intent in data["intents"]:
    tag = intent["tag"]
    patterns = intent["patterns"]
    responses = intent["responses"]

    for pattern in patterns:
        for response in responses:
            cur.execute("""
            INSERT INTO intents (id, tag, pattern, response)
            VALUES (%s, %s, %s, %s)
            """, (
                str(uuid.uuid4()),
                tag,
                pattern,
                response
            ))

conn.commit()
print("Intents migrated ")

cur.close()
conn.close()