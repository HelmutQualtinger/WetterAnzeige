from flask import Flask, render_template, jsonify, request
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT')),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/countries')
def get_countries():
    """Get all unique countries from weather_data"""
    conn = get_db_connection()
    countries = []
    if conn:
        cursor = conn.cursor()
        query = "SELECT DISTINCT country FROM weather_data ORDER BY country"
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        countries = [row[0] for row in results if row[0]]
    return jsonify(countries)

@app.route('/api/cantons')
def get_cantons():
    """Get all cantons for a specific country"""
    country = request.args.get('country', '')
    conn = get_db_connection()
    cantons = []
    if conn and country:
        cursor = conn.cursor()
        query = "SELECT DISTINCT canton FROM weather_data WHERE country = %s ORDER BY canton"
        cursor.execute(query, (country,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        cantons = [row[0] for row in results if row[0]]
    return jsonify(cantons)

@app.route('/api/cities')
def get_cities():
    """Get all cities for a specific country and canton"""
    country = request.args.get('country', '')
    canton = request.args.get('canton', '')
    conn = get_db_connection()
    cities = []
    if conn and country and canton:
        cursor = conn.cursor()
        query = "SELECT DISTINCT city FROM weather_data WHERE country = %s AND canton = %s ORDER BY city"
        cursor.execute(query, (country, canton))
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        cities = [row[0] for row in results if row[0]]
    return jsonify(cities)

@app.route('/api/weather')
def get_weather():
    """Get weather data for selected location"""
    country = request.args.get('country', 'AT')
    canton = request.args.get('canton', 'Vorarlberg')
    city = request.args.get('city', 'Feldkirch')

    conn = get_db_connection()
    data = {}
    if conn:
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT * FROM weather_data
            WHERE city = %s
            AND canton = %s
            AND country = %s
            ORDER BY dt DESC
            LIMIT 1
        """
        cursor.execute(query, (city, canton, country))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            data = result
        else:
            data = {"error": "Keine Daten gefunden"}
    else:
        data = {"error": "Datenbankverbindung fehlgeschlagen"}

    return jsonify(data)

if __name__ == '__main__':
    print("Starting Flask app on port 5050...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5051)
    except Exception as e:
        print(f"Failed to run app: {e}")