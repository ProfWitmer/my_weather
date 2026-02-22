"""Geocoding service for converting locations to coordinates."""
import requests
import time
from typing import Tuple, Optional


class GeocodingService:
    _last_request_time = 0
    _min_request_interval = 1.0  # Nominatim requires min 1 second between requests
    """Service for geocoding locations."""

    @staticmethod
    def _rate_limit():
        """Enforce rate limiting for Nominatim API (max 1 request per second)."""
        current_time = time.time()
        time_since_last_request = current_time - GeocodingService._last_request_time

        if time_since_last_request < GeocodingService._min_request_interval:
            time.sleep(GeocodingService._min_request_interval - time_since_last_request)

        GeocodingService._last_request_time = time.time()

    @staticmethod
    def geocode_zip(zip_code: str) -> Optional[Tuple[float, float, str]]:
        """
        Convert ZIP code to coordinates using Nominatim API.
        Returns (latitude, longitude, location_name) or None if not found.
        """
        try:
            GeocodingService._rate_limit()

            url = 'https://nominatim.openstreetmap.org/search'
            params = {
                'postalcode': zip_code,
                'country': 'US',
                'format': 'json',
                'limit': 1
            }
            headers = {
                'User-Agent': 'MyWeatherApp/1.0'
            }

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data:
                result = data[0]
                return (
                    float(result['lat']),
                    float(result['lon']),
                    result.get('display_name', zip_code)
                )
            return None
        except Exception as e:
            print(f"Error geocoding zip code {zip_code}: {e}")
            return None

    @staticmethod
    def geocode_city(city_name: str) -> Optional[Tuple[float, float, str]]:
        """
        Convert city name to coordinates using Nominatim API.
        Supports formats like "City Name" or "City, State".
        Returns (latitude, longitude, location_name) or None if not found.
        """
        try:
            GeocodingService._rate_limit()

            url = 'https://nominatim.openstreetmap.org/search'

            # Parse city and state if provided in "City, State" format
            parts = [p.strip() for p in city_name.split(',')]
            params = {
                'format': 'json',
                'limit': 1,
                'country': 'US'
            }

            if len(parts) == 2:
                # Format: "City, State"
                params['city'] = parts[0]
                params['state'] = parts[1]
            else:
                # Just city name
                params['city'] = city_name

            headers = {
                'User-Agent': 'MyWeatherApp/1.0'
            }

            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data:
                result = data[0]
                return (
                    float(result['lat']),
                    float(result['lon']),
                    result.get('display_name', city_name)
                )
            return None
        except Exception as e:
            print(f"Error geocoding city {city_name}: {e}")
            return None

    @staticmethod
    def geocode(location: str) -> Optional[Tuple[float, float, str]]:
        """
        Geocode a location (try as ZIP first, then as city name).
        Returns (latitude, longitude, location_name) or None if not found.
        """
        # Try as ZIP code first (5 digits)
        if location.strip().isdigit() and len(location.strip()) == 5:
            result = GeocodingService.geocode_zip(location.strip())
            if result:
                return result

        # Try as city name
        return GeocodingService.geocode_city(location)
