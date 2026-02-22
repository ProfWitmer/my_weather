"""Configuration for the weather application."""
import os

class Config:
    """Application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL')  # PostgreSQL URL for production
    DATABASE = os.path.join(os.path.dirname(__file__), 'weather.db')  # SQLite for local dev

    CACHE_TIMEOUT = 600  # 10 minutes in seconds
    WEATHER_API_BASE = 'https://api.weather.gov'
    WEATHER_API_USER_AGENT = '(MyWeatherApp, contact@example.com)'
