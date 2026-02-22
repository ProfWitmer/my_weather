"""Database initialization and management."""
import os
import sqlite3
from flask import g
from config import Config


class DatabaseWrapper:
    """Wrapper to provide unified interface for SQLite and PostgreSQL."""

    def __init__(self, conn, is_postgres=False):
        self.conn = conn
        self.is_postgres = is_postgres

    def execute(self, query, params=()):
        """Execute a query and return cursor."""
        if self.is_postgres:
            from psycopg2.extras import RealDictCursor
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        else:
            cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def commit(self):
        """Commit transaction."""
        self.conn.commit()

    def close(self):
        """Close connection."""
        self.conn.close()


def get_db():
    """Get database connection (PostgreSQL in production, SQLite locally)."""
    if 'db' not in g:
        if Config.DATABASE_URL:
            # PostgreSQL for production
            import psycopg2
            conn = psycopg2.connect(Config.DATABASE_URL)
            g.db = DatabaseWrapper(conn, is_postgres=True)
        else:
            # SQLite for local development
            conn = sqlite3.connect(
                Config.DATABASE,
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            conn.row_factory = sqlite3.Row
            g.db = DatabaseWrapper(conn, is_postgres=False)
    return g.db


def close_db(e=None):
    """Close database connection."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    """Initialize the database schema."""
    if Config.DATABASE_URL:
        # PostgreSQL initialization
        import psycopg2
        db = psycopg2.connect(Config.DATABASE_URL)
        cursor = db.cursor()

        # Table for saved locations
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                latitude REAL NOT NULL,
                longitude REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Table for weather cache
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather_cache (
                id SERIAL PRIMARY KEY,
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
                id SERIAL PRIMARY KEY,
                preference_key TEXT UNIQUE NOT NULL,
                preference_value TEXT NOT NULL
            )
        ''')

        # Set default preference for display type
        cursor.execute('''
            INSERT INTO preferences (preference_key, preference_value)
            VALUES ('display_type', 'temperature')
            ON CONFLICT (preference_key) DO NOTHING
        ''')

        db.commit()
        db.close()
    else:
        # SQLite initialization
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
