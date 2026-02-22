"""Database initialization and management."""
import sqlite3
from flask import g
from config import Config


def get_db():
    """Get database connection."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            Config.DATABASE,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database schema."""
    db = sqlite3.connect(Config.DATABASE)
    cursor = db.cursor()

    # Table for saved locations
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS locations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table for weather cache
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            cache_type TEXT NOT NULL,
            data TEXT NOT NULL,
            cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(latitude, longitude, cache_type)
        )
    ''')

    # Table for user preferences
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE NOT NULL,
            preference_value TEXT NOT NULL
        )
    ''')

    # Set default preference for display type
    cursor.execute('''
        INSERT OR IGNORE INTO preferences (preference_key, preference_value)
        VALUES ('display_type', 'temperature')
    ''')

    db.commit()
    db.close()


if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
