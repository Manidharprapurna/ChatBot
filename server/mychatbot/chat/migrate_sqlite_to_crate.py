import sqlite3
import psycopg2

# SQLite connection
sqlite_conn = sqlite3.connect("db.sqlite3")
sqlite_cursor = sqlite_conn.cursor()

# CrateDB connection
crate_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="crate",
    password="",
    database="doc"
)
crate_cursor = crate_conn.cursor()

# Fetch only active FAQs
sqlite_cursor.execute("""
SELECT id, question, answer, created_at 
FROM chat_faq
WHERE is_active = 1
""")

rows = sqlite_cursor.fetchall()

print(f"Total rows: {len(rows)}")

# Insert into CrateDB
for row in rows:
    crate_cursor.execute("""
    INSERT INTO chat_logs (id, message, response, intent, created_at)
    VALUES (%s, %s, %s, %s, %s)
    """, (
        str(row[0]),     # id (string for CrateDB)
        row[1],          # question → message
        row[2],          # answer → response
        "faq",           # intent (default)
        row[3]           # created_at
    ))

crate_conn.commit()

print("Migration completed ")

sqlite_conn.close()
crate_conn.close()