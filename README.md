# My Weather

A sophisticated Flask web application for displaying weather information for US locations using the weather.gov API.

## Features

- **Location Search**: Search by ZIP code or city name
- **Saved Locations**: Save favorite locations for quick access
- **Current Conditions**: View real-time weather data
- **10-Day Forecast**: Detailed daily forecast with weather icons
- **Hourly Forecast**: Hour-by-hour forecast for the next 48 hours
- **Animated Radar**: View animated radar maps for your location
- **Customizable Display**: Choose to display temperature, wind, or precipitation data
- **Smart Caching**: Weather data is cached for 10 minutes to reduce API calls
- **Weather Icons**: Beautiful emoji-based weather icons

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd my_weather
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python database.py
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to:
```
http://localhost:5000
```

## Usage

### Adding a Location

1. Enter a ZIP code (e.g., "10001") or city name (e.g., "New York, NY") in the search box
2. Click "Search"
3. The location will be automatically saved to your locations list

### Viewing Weather

- Click on any saved location to view current conditions
- Use the dropdown menu to switch between temperature, wind, and precipitation displays
- Click on "10-Day Forecast" to see the extended forecast
- Click on "Hourly" to see the hour-by-hour forecast
- Click on "Radar" to view animated radar maps

### Managing Locations

- Click the "✕" button next to any location to delete it from your saved locations
- Click on a location name to switch to that location

## Project Structure

```
my_weather/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # Database initialization
├── models.py                   # Data models (Location, WeatherCache, Preference)
├── requirements.txt            # Python dependencies
├── weather.db                  # SQLite database (created on first run)
├── services/
│   ├── geocoding_service.py   # Geocoding logic
│   └── weather_service.py     # Weather API integration
├── static/
│   └── css/
│       └── style.css          # Application styles
└── templates/
    ├── base.html              # Base template
    ├── index.html             # Home page
    ├── forecast.html          # 10-day forecast
    ├── hourly.html            # Hourly forecast
    └── radar.html             # Radar maps
```

## API Information

This application uses the following free APIs:

- **weather.gov API**: For weather data (current conditions, forecasts, radar)
- **US Census Geocoding API**: For converting ZIP codes and city names to coordinates

No API keys are required for these services.

## Technologies Used

- **Flask**: Web framework
- **SQLite3**: Database
- **weather.gov API**: Weather data source
- **US Census Geocoding API**: Location geocoding
- **Pure CSS**: Styling (no frameworks)

## Configuration

You can modify settings in `config.py`:

- `CACHE_TIMEOUT`: Cache duration in seconds (default: 600 = 10 minutes)
- `DATABASE`: Database file location
- `SECRET_KEY`: Flask secret key (change in production)

## License

This project is open source and available for educational purposes.
