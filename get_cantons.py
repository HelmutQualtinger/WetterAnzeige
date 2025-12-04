import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env Datei
load_dotenv()

config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT')),
    'database': os.getenv('DB_NAME'),
    'raise_on_warnings': True
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    cursor.execute("SELECT DISTINCT canton, country FROM location_table")
    canton_country_combinations = cursor.fetchall()
    
    print(f"Einzigartige Kombinationen aus Land und Kanton in der Tabelle 'location_table':")
    for canton, country in canton_country_combinations:
        print(f"- Land: {country}, Kanton: {canton}")

except Error as e:
    print(f"MySQL Fehler: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
