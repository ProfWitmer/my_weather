"""Weather service for fetching data from weather.gov API."""
import requests
from typing import Dict, Optional
from config import Config
from models import WeatherCache


class WeatherService:
    """Service for fetching weather data from weather.gov."""

    @staticmethod
    def _make_request(url: str) -> Optional[Dict]:
        """Make a request to weather.gov API."""
        try:
            headers = {
                'User-Agent': Config.WEATHER_API_USER_AGENT,
                'Accept': 'application/json'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
            return None

    @staticmethod
    def get_gridpoint(latitude: float, longitude: float) -> Optional[Dict]:
        """Get gridpoint data for a location."""
        # Check cache first
        cached = WeatherCache.get(latitude, longitude, 'gridpoint')
        if cached:
            return cached

        url = f"{Config.WEATHER_API_BASE}/points/{latitude},{longitude}"
        data = WeatherService._make_request(url)

        if data:
            WeatherCache.set(latitude, longitude, 'gridpoint', data)

        return data

    @staticmethod
    def get_forecast(latitude: float, longitude: float) -> Optional[Dict]:
        """Get 10-day forecast for a location."""
        # Check cache first
        cached = WeatherCache.get(latitude, longitude, 'forecast')
        if cached:
            return cached

        # Get gridpoint first
        gridpoint = WeatherService.get_gridpoint(latitude, longitude)
        if not gridpoint or 'properties' not in gridpoint:
            return None

        forecast_url = gridpoint['properties'].get('forecast')
        if not forecast_url:
            return None

        data = WeatherService._make_request(forecast_url)

        if data:
            WeatherCache.set(latitude, longitude, 'forecast', data)

        return data

    @staticmethod
    def get_hourly_forecast(latitude: float, longitude: float) -> Optional[Dict]:
        """Get hourly forecast for a location."""
        # Check cache first
        cached = WeatherCache.get(latitude, longitude, 'hourly')
        if cached:
            return cached

        # Get gridpoint first
        gridpoint = WeatherService.get_gridpoint(latitude, longitude)
        if not gridpoint or 'properties' not in gridpoint:
            return None

        hourly_url = gridpoint['properties'].get('forecastHourly')
        if not hourly_url:
            return None

        data = WeatherService._make_request(hourly_url)

        if data:
            WeatherCache.set(latitude, longitude, 'hourly', data)

        return data

    @staticmethod
    def get_current_conditions(latitude: float, longitude: float) -> Optional[Dict]:
        """Get current weather conditions."""
        # Check cache first
        cached = WeatherCache.get(latitude, longitude, 'current')
        if cached:
            return cached

        # Get gridpoint first
        gridpoint = WeatherService.get_gridpoint(latitude, longitude)
        if not gridpoint or 'properties' not in gridpoint:
            return None

        # Get observation stations
        stations_url = gridpoint['properties'].get('observationStations')
        if not stations_url:
            return None

        stations_data = WeatherService._make_request(stations_url)
        if not stations_data or 'features' not in stations_data:
            return None

        # Get latest observation from first station
        if stations_data['features']:
            station_id = stations_data['features'][0]['properties']['stationIdentifier']
            obs_url = f"{Config.WEATHER_API_BASE}/stations/{station_id}/observations/latest"
            data = WeatherService._make_request(obs_url)

            if data:
                WeatherCache.set(latitude, longitude, 'current', data)

            return data

        return None

    @staticmethod
    def get_radar_station(latitude: float, longitude: float) -> Optional[str]:
        """Get the nearest radar station for a location."""
        gridpoint = WeatherService.get_gridpoint(latitude, longitude)
        if gridpoint and 'properties' in gridpoint:
            return gridpoint['properties'].get('radarStation')
        return None

    @staticmethod
    def get_alerts(latitude: float, longitude: float) -> Optional[Dict]:
        """Get active weather alerts for a location."""
        # Check cache first (cache for 5 minutes since alerts change frequently)
        cached = WeatherCache.get(latitude, longitude, 'alerts')
        if cached:
            return cached

        # Get alerts for the location
        url = f"{Config.WEATHER_API_BASE}/alerts/active?point={latitude},{longitude}"
        data = WeatherService._make_request(url)

        if data:
            WeatherCache.set(latitude, longitude, 'alerts', data)

        return data
