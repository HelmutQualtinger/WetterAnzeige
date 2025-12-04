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

def update_coordinates(filename):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        updated_count = 0
        skipped_count = 0
        
        with open(filename, 'r') as f:
            # Skip header
            next(f)
            
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 5:
                    city = parts[0].strip()
                    canton = parts[1].strip()
                    country = parts[2].strip()
                    lat_str = parts[3].strip()
                    lon_str = parts[4].strip()
                    
                    if lat_str == "Not Found" or lon_str == "Not Found":
                        print(f"Skipping {city}, {country}: Coordinates not found in file.")
                        skipped_count += 1
                        continue
                        
                    try:
                        lat = float(lat_str)
                        lon = float(lon_str)
                        
                        query = """
                            UPDATE location_table 
                            SET lat = %s, lon = %s 
                            WHERE city = %s AND canton = %s AND country = %s
                        """
                        cursor.execute(query, (lat, lon, city, canton, country))
                        updated_count += 1
                        
                    except ValueError:
                        print(f"Skipping {city}, {country}: Invalid coordinates '{lat_str}', '{lon_str}'")
                        skipped_count += 1
        
        conn.commit()
        print(f"\nUpdate complete.")
        print(f"Updated: {updated_count}")
        print(f"Skipped: {skipped_count}")

    except Error as e:
        print(f"MySQL Fehler: {e}")
    except FileNotFoundError:
        print(f"File {filename} not found.")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    update_coordinates('coordinates.txt')
