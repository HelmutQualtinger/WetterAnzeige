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
    
    cursor.execute("SELECT DISTINCT city, canton, country FROM location_table ORDER BY country, canton, city")
    cities = cursor.fetchall()
    
    with open('cities_list.txt', 'w') as f:
        for city, canton, country in cities:
            f.write(f"{city}, {canton}, {country}\n")
            
    print(f"Exported {len(cities)} cities to cities_list.txt")

except Error as e:
    print(f"MySQL Fehler: {e}")
finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()

