import sqlite3

def init_db():
    conn = sqlite3.connect('plagiarism.db')
    c = conn.cursor()

    # Drop old table if exists (optional safety)
    c.execute('DROP TABLE IF EXISTS submissions')

    # Create new table for storing content
    c.execute('''
        CREATE TABLE submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully.")

if __name__ == '__main__':
    init_db()
