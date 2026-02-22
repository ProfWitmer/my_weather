"""Main Flask application for weather display."""
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from config import Config
from database import get_db, close_db, init_db
from models import Location, Preference
from services.weather_service import WeatherService
from services.geocoding_service import GeocodingService
import os

app = Flask(__name__)
app.config.from_object(Config)
app.teardown_appcontext(close_db)

# Initialize database if it doesn't exist
if not os.path.exists(Config.DATABASE):
    init_db()


@app.route('/')
def index():
    """Main page - weather display."""
    locations = Location.get_all()
    display_type = Preference.get('display_type', 'temperature')

    # Get current weather if a location is selected
    location_id = request.args.get('location_id', type=int)
    weather_data = None
    current_location = None
    error = None

    if location_id:
        current_location = Location.get_by_id(location_id)
        if current_location:
            weather_data = WeatherService.get_current_conditions(
                current_location['latitude'],
                current_location['longitude']
            )
            if not weather_data:
                error = "Unable to fetch weather data"

    return render_template(
        'index.html',
        locations=locations,
        current_location=current_location,
        weather_data=weather_data,
        display_type=display_type,
        error=error
    )


@app.route('/search', methods=['POST'])
def search_location():
    """Search for a location and add it to saved locations."""
    location_query = request.form.get('location', '').strip()

    if not location_query:
        return redirect(url_for('index'))

    # Geocode the location
    result = GeocodingService.geocode(location_query)

    if result:
        latitude, longitude, name = result

        # Check if location already exists
        existing_location = Location.find_by_coordinates(latitude, longitude)

        if existing_location:
            # Use existing location instead of adding duplicate
            location_id = existing_location['id']
        else:
            # Add to saved locations
            location_id = Location.add(name, latitude, longitude)

        return redirect(url_for('index', location_id=location_id))
    else:
        return render_template(
            'index.html',
            locations=Location.get_all(),
            error=f"Location '{location_query}' not found. Please try a different zip code or city name.",
            display_type=Preference.get('display_type', 'temperature')
        )


@app.route('/location/<int:location_id>/delete', methods=['POST'])
def delete_location(location_id):
    """Delete a saved location."""
    Location.delete(location_id)
    return redirect(url_for('index'))


@app.route('/forecast/<int:location_id>')
def forecast(location_id):
    """Display 10-day forecast for a location."""
    location = Location.get_by_id(location_id)
    if not location:
        return redirect(url_for('index'))

    forecast_data = WeatherService.get_forecast(
        location['latitude'],
        location['longitude']
    )

    display_type = Preference.get('display_type', 'temperature')

    return render_template(
        'forecast.html',
        location=location,
        forecast_data=forecast_data,
        display_type=display_type,
        locations=Location.get_all()
    )


@app.route('/hourly/<int:location_id>')
def hourly(location_id):
    """Display hourly forecast for a location."""
    location = Location.get_by_id(location_id)
    if not location:
        return redirect(url_for('index'))

    hourly_data = WeatherService.get_hourly_forecast(
        location['latitude'],
        location['longitude']
    )

    display_type = Preference.get('display_type', 'temperature')

    return render_template(
        'hourly.html',
        location=location,
        hourly_data=hourly_data,
        display_type=display_type,
        locations=Location.get_all()
    )


@app.route('/radar/<int:location_id>')
def radar(location_id):
    """Display radar map for a location."""
    location = Location.get_by_id(location_id)
    if not location:
        return redirect(url_for('index'))

    radar_station = WeatherService.get_radar_station(
        location['latitude'],
        location['longitude']
    )

    return render_template(
        'radar.html',
        location=location,
        radar_station=radar_station,
        locations=Location.get_all()
    )


@app.route('/preferences', methods=['POST'])
def set_preference():
    """Set user preference for display type."""
    display_type = request.form.get('display_type', 'temperature')
    Preference.set('display_type', display_type)

    # Redirect back to the page they came from
    return redirect(request.referrer or url_for('index'))


@app.template_filter('celsius_to_fahrenheit')
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    if celsius is None:
        return None
    return round((celsius * 9/5) + 32, 1)


@app.template_filter('get_weather_icon')
def get_weather_icon(forecast):
    """Get appropriate weather icon based on forecast."""
    if not forecast:
        return 'cloud'

    desc = forecast.lower()

    if 'sunny' in desc or 'clear' in desc:
        return 'sun'
    elif 'rain' in desc or 'shower' in desc:
        return 'umbrella'
    elif 'storm' in desc or 'thunder' in desc:
        return 'storm'
    elif 'snow' in desc:
        return 'snowflake'
    elif 'cloud' in desc or 'overcast' in desc:
        return 'cloud'
    elif 'fog' in desc or 'mist' in desc:
        return 'fog'
    elif 'wind' in desc:
        return 'wind'
    else:
        return 'cloud'


@app.template_filter('weather_icon_html')
def weather_icon_html(icon_name):
    """Convert icon name to HTML emoji."""
    icons = {
        'sun': '☀️',
        'umbrella': '☔',
        'storm': '⛈️',
        'snowflake': '❄️',
        'cloud': '☁️',
        'fog': '🌫️',
        'wind': '💨'
    }
    return icons.get(icon_name, '☁️')


if __name__ == '__main__':
    # Development server only - use gunicorn in production
    app.run(debug=True, host='0.0.0.0', port=5003)
