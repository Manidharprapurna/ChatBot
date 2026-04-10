import uuid
import datetime
import psycopg2

from chat.chunk_utils import split_into_chunks

# Connect CrateDB
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="crate",
    password="",
    database="doc"
)

cur = conn.cursor()

# STEP 1: Read data
cur.execute("SELECT message, response FROM chat_logs")
rows = cur.fetchall()

print(f"Total rows: {len(rows)}")

# STEP 2: Clear old chunks
cur.execute("DELETE FROM chat_chunks")
conn.commit()

# STEP 3: Create chunks (QUESTION + ANSWER)
for message, response in rows:

    full_text = f"{message}. {response}"  

    chunks = split_into_chunks(full_text, chunk_size=20)

    print("CHUNKS:", chunks)  # debug

    for chunk in chunks:
        cur.execute("""
        INSERT INTO chat_chunks (id, chunk, source, created_at)
        VALUES (%s, %s, %s, %s)
        """, (
            str(uuid.uuid4()),
            chunk.strip(),
            message,
            datetime.datetime.now()
        ))

conn.commit()

print("Chunks recreated successfully ")

cur.close()
conn.close()