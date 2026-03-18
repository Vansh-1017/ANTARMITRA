"""Handles all SQLite database operations for the application."""

import sqlite3
import pandas as pd
import os

os.makedirs("database", exist_ok=True)
DB_PATH = os.path.join("database", "antarmitra.db")

def update_db_schema() -> None:
    """Ensures the database has the required columns."""
    with sqlite3.connect(DB_PATH) as conn:
        try:
            conn.execute("ALTER TABLE journal_entries ADD COLUMN trigger_category TEXT")
        except sqlite3.OperationalError:
            pass

def get_journal_data() -> pd.DataFrame:
    """Retrieves all journal entries as a Pandas DataFrame."""
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
        
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query("SELECT * FROM journal_entries ORDER BY entry_date DESC", conn)

def save_journal_entry(user_input: str, mood_score: float, motivation: str, trigger: str) -> None:
    """Inserts a new analyzed journal entry into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            INSERT INTO journal_entries (user_text, ml_sentiment_score, ai_suggestion, trigger_category) 
            VALUES (?, ?, ?, ?)
        ''', (user_input, mood_score, motivation, trigger))
        conn.commit()