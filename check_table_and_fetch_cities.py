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
    
    # Check columns
    cursor.execute("SHOW COLUMNS FROM location_table")
    columns = cursor.fetchall()
    print("Columns in location_table:")
    for col in columns:
        print(col)
        
    # Get cities
    cursor.execute("SELECT DISTINCT city, country, canton FROM location_table")
    cities = cursor.fetchall()
    
    print(f"\nFound {len(cities)} cities.")
    # Print first few to verify
    for i, city in enumerate(cities[:5]):
        print(city)

except Error as e:
    print(f"MySQL Fehler: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()
