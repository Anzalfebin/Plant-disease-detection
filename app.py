from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np
import requests
import os
from datetime import datetime, timedelta

# --- NEW: Manual .env file loading function ---
def load_manual_env(file_path='.env'):
    """
    Manually reads a .env file and loads variables into the environment.
    This is a fallback for when python-dotenv fails.
    """
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    # Remove potential quotes from the value
                    value = value.strip().strip('"').strip("'")
                    os.environ[key.strip()] = value
                    # print(f"Manually loaded: {key.strip()}") # You can uncomment this for debugging
    except FileNotFoundError:
        print(f"Warning: {file_path} file not found. API keys will not be loaded.")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

# --- Call the new manual loading function ---
load_manual_env()

# --- API Keys and Endpoints (This part remains the same) ---
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# --- MODIFIED: Switched to the 5-day forecast API endpoint ---
WEATHER_URL = "http://api.openweathermap.org/data/2.5/forecast?q={}&appid={}&units=metric"
NEWS_URL = "https://newsapi.org/v2/everything?q=agriculture India farm government schemes&sortBy=publishedAt&language=en&apiKey={}"

# --- Create Flask App ---
app = Flask(__name__)

# --- Load Machine Learning Model ---
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# ... (The rest of the file is exactly the same as before) ...

# --- Helper Data ---
CROP_DETAILS = {
    'rice': {
        'description': 'Rice is a staple food for over half of the world\'s population. It requires significant water and warm temperatures to grow.',
        'season': 'Kharif (June - October)',
        'common_pests': 'Stem Borer, Brown Planthopper'
    },
    'maize': {
        'description': 'Maize, known as corn, is a versatile crop used for food, animal feed, and biofuel. It thrives in sunny and warm conditions.',
        'season': 'Kharif & Rabi',
        'common_pests': 'Fall Armyworm, Corn Borer'
    },
    'default': {
        'description': 'Information for this crop is not yet available.',
        'season': 'N/A',
        'common_pests': 'N/A'
    }
}

GOV_SCHEMES = {
    'rice': [
        {'name': 'Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)', 'link': 'https://pmkisan.gov.in/'},
        {'name': 'Minimum Support Price (MSP) for Paddy', 'link': 'https://farmer.gov.in/msp.aspx'}
    ],
    'maize': [
        {'name': 'National Food Security Mission (NFSM)', 'link': 'https://www.nfsm.gov.in/'},
        {'name': 'Minimum Support Price (MSP) for Maize', 'link': 'https://farmer.gov.in/msp.aspx'}
    ],
    'default': [
        {'name': 'Kisan Credit Card (KCC)', 'link': 'https://www.agricoop.nic.in/en/KisanCreditCard'}
    ]
}

# --- Flask Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        features = [float(x) for x in request.form.values()]
        final_features = [np.array(features)]
        prediction = model.predict(final_features)
        
        predicted_crop = prediction[0]
        crop_lower = predicted_crop.lower()
        
        crop_details = CROP_DETAILS.get(crop_lower, CROP_DETAILS['default'])
        schemes = GOV_SCHEMES.get(crop_lower, GOV_SCHEMES['default'])
        
        return render_template(
            'index.html', 
            prediction_text=f'Recommended Crop: {predicted_crop.capitalize()}',
            crop_name=crop_lower,
            crop_details=crop_details,
            schemes=schemes
        )
    except Exception as e:
        return render_template('index.html', prediction_text=f'Error predicting: {e}')

# --- NEW: Weather processing and alert generation logic ---
def process_forecast(forecast_data):
    daily_forecasts = {}
    alerts = []
    
    city_name = forecast_data.get('city', {}).get('name', 'N/A')
    
    for entry in forecast_data['list']:
        dt = datetime.fromtimestamp(entry['dt'])
        day = dt.strftime('%Y-%m-%d')
        
        if day not in daily_forecasts:
            daily_forecasts[day] = {
                'day_name': dt.strftime('%A'),
                'temps': [],
                'weather': []
            }
        
        daily_forecasts[day]['temps'].append(entry['main']['temp'])
        daily_forecasts[day]['weather'].append(entry['weather'][0])
        
        # Alert generation logic
        if entry['weather'][0]['id'] < 300: # Thunderstorm
            alerts.append(f"Caution: Thunderstorm predicted on {dt.strftime('%A, %b %d')}.")
        if entry['main']['temp'] > 38: # Extreme heat
             alerts.append(f"Alert: Extreme heat above 38°C on {dt.strftime('%A, %b %d')}. Ensure proper irrigation.")
        if entry.get('wind', {}).get('speed', 0) > 15: # High wind speed in m/s
             alerts.append(f"Warning: Strong winds (>50 km/h) expected on {dt.strftime('%A, %b %d')}. Protect vulnerable crops.")

    processed = []
    for day, data in daily_forecasts.items():
        if len(processed) >= 4: # Limit to 4 days
            break
        processed.append({
            'day': data['day_name'],
            'min_temp': round(min(data['temps'])),
            'max_temp': round(max(data['temps'])),
            # Get the weather from the midday forecast for a representative icon
            'icon': next((w['icon'] for w in data['weather'] if '12:00:00' in day), data['weather'][0]['icon']),
            'description': next((w['description'] for w in data['weather'] if '12:00:00' in day), data['weather'][0]['description'])
        })
        
    # Remove duplicate alerts
    unique_alerts = sorted(list(set(alerts)))

    return {"city": city_name, "forecasts": processed, "alerts": unique_alerts}


@app.route('/weather')
def get_weather():
    city = request.args.get('city', 'Delhi')
    if not WEATHER_API_KEY:
        return jsonify({"error": "Weather API key not configured"}), 500
    
    try:
        response = requests.get(WEATHER_URL.format(city, WEATHER_API_KEY))
        response.raise_for_status()
        raw_data = response.json()
        processed_data = process_forecast(raw_data)
        return jsonify(processed_data)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Error processing data: {e}"}), 500

@app.route('/news')
def get_news():
    if not NEWS_API_KEY:
        return jsonify({"error": "News API key not configured"}), 500
    
    try:
        response = requests.get(NEWS_URL.format(NEWS_API_KEY))
        response.raise_for_status()
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)