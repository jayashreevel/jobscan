# init_db.py

import sqlite3

# Connect to database (creates if not exists)
conn = sqlite3.connect("job_results.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_title TEXT,
        job_description TEXT,
        job_url TEXT,
        prediction TEXT,
        timestamp TEXT
    )
''')

conn.commit()
conn.close()

print("✅ Database initialized successfully.")
