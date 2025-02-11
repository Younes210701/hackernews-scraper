import sqlite3
import os

DB_PATH = "data/hackernews.db"

def init_db():
    """
    Initialize the SQLite the database
    """
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        title TEXT,
        link TEXT,
        points INTEGER,
        comments INTEGER
    )
    """)

    conn.commit()
    conn.close()

def save_to_db(articles):
    """
    Save the articles in the SQLite base
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for art in articles:
        cursor.execute("""
        INSERT OR IGNORE INTO articles (id, title, link, points, comments)
        VALUES (?, ?, ?, ?, ?)
        """, (art["id"], art["title"], art["link"], art["points"], art["comments"]))

    conn.commit()
    conn.close()