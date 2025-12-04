import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

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
    
    cursor.execute("SELECT city, canton, country FROM location_table WHERE lat IS NULL OR lon IS NULL OR lat = 0 OR lon = 0")
    missing_coords = cursor.fetchall()
    
    print(f"Cities still missing coordinates in DB: {len(missing_coords)}")
    for city in missing_coords:
         print(city)

except Error as e:
    print(f"MySQL Fehler: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
