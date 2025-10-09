"""Check tables in SQLite database."""
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print("Database tables:")
for table in tables:
    print(f"  - {table}")
    # Count rows
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    print(f"    Rows: {count}")
conn.close()
