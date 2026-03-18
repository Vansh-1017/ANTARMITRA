import sqlite3
import os

# Define the path where the offline database will live
DB_DIR = "database"
DB_PATH = os.path.join(DB_DIR, "antarmitra.db")

def create_database():
    # 1. Ensure the database folder exists
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    # 2. Connect to SQLite (this automatically creates the .db file if it is missing)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 3. Write the SQL command to create our table
    # This table stores the date, what the user wrote, the ML score, and the AI's advice
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_text TEXT NOT NULL,
            ml_sentiment_score REAL,
            ai_suggestion TEXT
        )
    ''')

    # 4. Save the changes and close the connection
    conn.commit()
    conn.close()
    
    print(f"Success! Secure offline database created at: {DB_PATH}")

if __name__ == "__main__":
    create_database()