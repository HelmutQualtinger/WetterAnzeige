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
    
    # Check for empty coordinates
    cursor.execute("SELECT city, country, canton FROM location_table WHERE lat IS NULL OR lon IS NULL OR lat = 0 OR lon = 0")
    missing_coords = cursor.fetchall()
    
    print(f"Cities with missing or zero coordinates: {len(missing_coords)}")
    for city in missing_coords[:10]:
         print(city)

    # Check for populated coordinates
    cursor.execute("SELECT count(*) FROM location_table WHERE lat IS NOT NULL AND lon IS NOT NULL AND lat != 0 AND lon != 0")
    populated_count = cursor.fetchone()[0]
    print(f"Cities with populated coordinates: {populated_count}")


except Error as e:
    print(f"MySQL Fehler: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
