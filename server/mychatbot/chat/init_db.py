from .cratedb import get_connection

conn = get_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS chat_logs (
    id TEXT PRIMARY KEY,
    message TEXT,
    response TEXT,
    intent TEXT,
    created_at TIMESTAMP
)
""")

conn.commit()
cur.close()
conn.close()

print("Table created successfully")