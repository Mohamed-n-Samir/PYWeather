import requests
import csv

# GeoNames API key (replace with your own)
GEONAMES_API_KEY = 'nash_pan'

# GeoNames endpoint to fetch country info
GEONAMES_COUNTRYINFO_URL = 'http://api.geonames.org/countryInfoJSON'

# Function to fetch country info from GeoNames
def get_country_info():
    params = {
        'username': GEONAMES_API_KEY  # GeoNames username
    }

    # Make the API request
    response = requests.get(GEONAMES_COUNTRYINFO_URL, params=params)
    data = response.json()

    if 'geonames' not in data:
        print("Error fetching country info.")
        return []

    # List of countries and their codes
    country_info = []
    for country in data['geonames']:
        # print(data['geonames'])
        country_name = country.get('countryName')
        country_code = country.get('countryCode')
        country_north = country.get('north')
        country_south = country.get('south')
        country_west = country.get('west')
        country_east = country.get('east')
        geonameId = country.get('geonameId')
        print(geonameId)
        if country_name and country_code:
            country_info.append((country_name, country_code, country_west,country_north, country_east, country_south, geonameId))

    return country_info

def save_countries_to_csv(countries):
    with open('./countries.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Country Name', 'Country Code', 'West', 'North', 'East', "South", "GeonameID"])
        for country_name, country_code,country_west,country_north, country_east, country_south, geonameId in countries:
            writer.writerow([country_name, country_code,country_west,country_north, country_east, country_south, geonameId])

# Fetch and print country info
country_info = get_country_info()
save_countries_to_csv(countries=country_info)
print("Country Name and Country Code:")
# for name, code in country_info:
#     print(f"{name}: {code}")
