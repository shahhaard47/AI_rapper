import sqlite3
import os

DB_PATH = "chat_data.db"

def init_db():
    """Initialize the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            username TEXT,
            chat_name TEXT,
            messages TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_chat(username, chat_name, messages):
    """Save or update a chat in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO chats (username, chat_name, messages)
        VALUES (?, ?, ?)
    """, (username, chat_name, str(messages)))
    conn.commit()
    conn.close()

def load_chats(username):
    """Load all chats for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT chat_name, messages FROM chats WHERE username = ?", (username,))
    chats = {row[0]: eval(row[1]) for row in cursor.fetchall()}
    conn.close()
    return chats
