# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

My Weather is a Flask web application that displays weather information for US locations using the weather.gov API. The application supports location search (ZIP code or city name), saved locations, current conditions, 10-day forecasts, hourly forecasts, and animated radar maps. Weather data is cached for 10 minutes to reduce API calls.

## Development Commands

### Database Initialization
```bash
python database.py
```
Initializes the SQLite database with required tables (locations, weather_cache, preferences).

### Run Development Server
```bash
python app.py
```
Starts Flask development server on http://localhost:5000

### Install Dependencies
```bash
pip install -r requirements.txt
```
Installs Flask, requests, and python-dateutil.

## Code Architecture

### Application Structure

The application follows a service-oriented architecture:

- **app.py**: Main Flask application with routes and template filters
- **config.py**: Configuration constants (cache timeout, API settings)
- **database.py**: Database connection management and initialization
- **models.py**: Data models (Location, WeatherCache, Preference) - all use static methods
- **services/**: Business logic layer
  - **geocoding_service.py**: Converts ZIP codes and city names to coordinates using US Census API
  - **weather_service.py**: Fetches weather data from weather.gov API with caching

### Data Flow

1. User searches for a location → GeocodingService converts to coordinates → Location saved to DB
2. User views weather → WeatherService checks cache → Fetches from API if expired → Caches result
3. Weather data retrieved in this order:
   - Get gridpoint data (contains forecast URLs and radar station)
   - Get current conditions from nearest observation station
   - Get forecast or hourly forecast from gridpoint URLs

### Database Schema

- **locations**: Stores saved locations with coordinates
- **weather_cache**: Caches API responses by lat/lon and type (gridpoint, forecast, hourly, current)
- **preferences**: Stores user preferences (display_type: temperature/wind/precipitation)

### Weather.gov API Integration

The weather.gov API requires a specific flow:
1. Call `/points/{lat},{lon}` to get gridpoint data
2. Extract forecast URLs and observation station URLs from gridpoint
3. Call specific endpoints for current conditions, forecast, hourly forecast
4. All requests must include User-Agent header (configured in Config.WEATHER_API_USER_AGENT)

### Template Filters

- `celsius_to_fahrenheit`: Converts temperature values
- `get_weather_icon`: Maps forecast text to icon names
- `weather_icon_html`: Converts icon names to emoji characters

### Caching Strategy

Cache timeout is 10 minutes (Config.CACHE_TIMEOUT). Each cache entry is identified by:
- Latitude/longitude (rounded)
- Cache type (gridpoint, forecast, hourly, current)

The WeatherCache model automatically checks expiration before returning cached data.
