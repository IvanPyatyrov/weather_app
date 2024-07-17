from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)

API_URL = "https://api.open-meteo.com/v1/forecast"
API_PARAMS = {
    "hourly": "temperature_2m",
    "current_weather": True
}

class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}")
        if response.status_code == 200:
            data = response.json()
            if data['results']:
                lat = data['results'][0]['latitude']
                lon = data['results'][0]['longitude']
                weather_response = requests.get(API_URL, params={**API_PARAMS, "latitude": lat, "longitude": lon})
                if weather_response.status_code == 200:
                    weather_data = weather_response.json()
                    new_search = SearchHistory(city=city)
                    db.session.add(new_search)
                    db.session.commit()
    search_history = SearchHistory.query.all()
    return render_template('index.html', weather=weather_data, history=search_history)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = SearchHistory.query.filter(SearchHistory.city.like(f'%{search}%')).all()
    results = [city.city for city in query]
    return jsonify(results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
