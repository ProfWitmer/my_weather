"""Data models for the weather application."""
from database import get_db
from datetime import datetime, timedelta
import json


class Location:
    """Model for saved locations."""

    @staticmethod
    def get_all():
        """Get all saved locations."""
        db = get_db()
        locations = db.execute(
            'SELECT * FROM locations ORDER BY created_at DESC'
        ).fetchall()
        return [dict(loc) for loc in locations]

    @staticmethod
    def get_by_id(location_id):
        """Get a location by ID."""
        db = get_db()
        location = db.execute(
            'SELECT * FROM locations WHERE id = ?',
            (location_id,)
        ).fetchone()
        return dict(location) if location else None

    @staticmethod
    def find_by_coordinates(latitude, longitude, tolerance=0.01):
        """
        Find a location by coordinates with tolerance.
        Returns the location if found within tolerance, None otherwise.
        """
        db = get_db()
        locations = Location.get_all()

        for loc in locations:
            lat_diff = abs(loc['latitude'] - latitude)
            lon_diff = abs(loc['longitude'] - longitude)

            if lat_diff <= tolerance and lon_diff <= tolerance:
                return loc

        return None

    @staticmethod
    def add(name, latitude, longitude):
        """Add a new location."""
        db = get_db()
        cursor = db.execute(
            'INSERT INTO locations (name, latitude, longitude) VALUES (?, ?, ?)',
            (name, latitude, longitude)
        )
        db.commit()
        return cursor.lastrowid

    @staticmethod
    def delete(location_id):
        """Delete a location."""
        db = get_db()
        db.execute('DELETE FROM locations WHERE id = ?', (location_id,))
        db.commit()


class WeatherCache:
    """Model for weather data cache."""

    @staticmethod
    def get(latitude, longitude, cache_type):
        """Get cached weather data if not expired."""
        db = get_db()
        cache = db.execute(
            'SELECT * FROM weather_cache WHERE latitude = ? AND longitude = ? AND cache_type = ?',
            (latitude, longitude, cache_type)
        ).fetchone()

        if cache:
            # SQLite returns datetime objects when PARSE_DECLTYPES is enabled
            cached_at = cache['cached_at']
            if isinstance(cached_at, str):
                # Handle string format if needed
                cached_at = datetime.fromisoformat(cached_at.replace(' ', 'T'))
            if datetime.now() - cached_at < timedelta(seconds=600):  # 10 minutes
                return json.loads(cache['data'])
        return None

    @staticmethod
    def set(latitude, longitude, cache_type, data):
        """Set cached weather data."""
        db = get_db()
        db.execute(
            '''INSERT OR REPLACE INTO weather_cache
               (latitude, longitude, cache_type, data, cached_at)
               VALUES (?, ?, ?, ?, ?)''',
            (latitude, longitude, cache_type, json.dumps(data), datetime.now())
        )
        db.commit()


class Preference:
    """Model for user preferences."""

    @staticmethod
    def get(key, default=None):
        """Get a preference value."""
        db = get_db()
        pref = db.execute(
            'SELECT preference_value FROM preferences WHERE preference_key = ?',
            (key,)
        ).fetchone()
        return pref['preference_value'] if pref else default

    @staticmethod
    def set(key, value):
        """Set a preference value."""
        db = get_db()
        db.execute(
            'INSERT OR REPLACE INTO preferences (preference_key, preference_value) VALUES (?, ?)',
            (key, value)
        )
        db.commit()
