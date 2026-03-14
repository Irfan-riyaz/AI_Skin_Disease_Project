import sqlite3

conn = sqlite3.connect('app.db')
cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print("Tables:", tables)

for table in tables:
    table_name = table[0]
    cur = conn.execute(f"PRAGMA table_info({table_name})")
    cols = cur.fetchall()
    print(f"\n{table_name}:")
    for col in cols:
        print(f"  {col}")

conn.close()
