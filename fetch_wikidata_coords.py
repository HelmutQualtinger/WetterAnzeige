import requests
import time

# Map country codes to Wikidata Q-IDs
COUNTRY_MAP = {
    'AT': 'Q40',
    'CH': 'Q39',
    'DE': 'Q183',
    'FR': 'Q142',
    'IT': 'Q38'
}

def load_cities(filename):
    cities_by_country = {code: [] for code in COUNTRY_MAP}
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    city = parts[0].strip()
                    canton = parts[1].strip()
                    country = parts[2].strip()
                    if country in cities_by_country:
                        cities_by_country[country].append({'city': city, 'canton': canton})
    except FileNotFoundError:
        print(f"File {filename} not found.")
    return cities_by_country

def fetch_coordinates(country_code, q_id, cities):
    print(f"Fetching coordinates for {len(cities)} cities in {country_code} ({q_id})...")
    
    # Prepare list of names for SPARQL VALUES clause
    # Escape quotes in names
    city_names = set()
    for c in cities:
        city_names.add(c['city'])
    
    # Construct VALUES string
    # Try German and English labels, and maybe without language tag?
    # Wikidata typically matches literal strings better if we are careful.
    # We will filter by label in the query.
    
    # To avoid huge query string, we might need to batch if too many.
    # 100 cities per batch is safe.
    
    city_names_list = list(city_names)
    batch_size = 50
    results = {}

    for i in range(0, len(city_names_list), batch_size):
        batch = city_names_list[i:i+batch_size]
        
        # Build the VALUES list
        # We check against rdfs:label with various languages.
        values_str = " ".join([f'"{name}"' for name in batch])
        values_str_de = " ".join([f'"{name}"@de' for name in batch])
        values_str_en = " ".join([f'"{name}"@en' for name in batch])
        values_str_fr = " ".join([f'"{name}"@fr' for name in batch])
        values_str_it = " ".join([f'"{name}"@it' for name in batch])
        
        # Query: Find items in the country that have one of these labels
        # and represent a human settlement (or similar).
        query = f"""
        SELECT ?label ?lat ?lon WHERE {{
          VALUES ?label {{ {values_str} {values_str_de} {values_str_en} {values_str_fr} {values_str_it} }}
          ?item rdfs:label ?label .
          ?item wdt:P17 wd:{q_id} . 
          ?item wdt:P625 ?coords .
          ?item p:P625 ?coordinate .
          ?coordinate psv:P625 ?coordinate_node .
          ?coordinate_node wikibase:geoLatitude ?lat .
          ?coordinate_node wikibase:geoLongitude ?lon .
        }}
        """
        print(query)
        url = 'https://query.wikidata.org/sparql'
        try:
            r = requests.get(url, params={'format': 'json', 'query': query})
            if r.status_code == 200:
                data = r.json()
                for item in data['results']['bindings']:
                    label = item['label']['value']
                    lat = item['lat']['value']
                    lon = item['lon']['value']
                    if label in batch:
                        results[label] = (lat, lon)
            else:
                print(f"Error: {r.status_code} - {r.text}")
        except Exception as e:
            print(f"Exception: {e}")
            try:
                 print(f"Keys available: {data['results']['bindings'][0].keys()}")
            except:
                 pass
            
        time.sleep(2) # Be nice to the API

    return results

def main():
    cities_by_country = load_cities('cities_list.txt')
    
    all_results = []
    
    for country, cities in cities_by_country.items():
        if not cities:
            continue
        
        q_id = COUNTRY_MAP[country]
        coords_map = fetch_coordinates(country, q_id, cities)
        
        # Match back to original list
        for c in cities:
            name = c['city']
            canton = c['canton']
            if name in coords_map:
                lat, lon = coords_map[name]
                # Format lat and lon to 4 decimal places
                formatted_lat = f"{float(lat):.5f}"
                formatted_lon = f"{float(lon):.5f}"
                all_results.append(f"{name}, {canton}, {country}, {formatted_lat}, {formatted_lon}")
            else:
                # If not found, output with empty or "Not Found"
                # But user wants "coordinates", maybe leave empty or try fallback?
                # I'll mark as Not Found for now
                all_results.append(f"{name}, {canton}, {country}, Not Found, Not Found")

    with open('coordinates.txt', 'w') as f:
        f.write("City, Canton, Country, Lat, Lon\n")
        for line in all_results:
            f.write(line + "\n")
            
    print("Done. Wrote coordinates.txt")

if __name__ == '__main__':
    main()
