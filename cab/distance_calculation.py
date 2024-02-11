import requests
from math import radians, sin, cos, sqrt, atan2

def get_coordinates(address):
    url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json"
    response = requests.get(url)
    data = response.json()
    if data:
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return latitude, longitude
    else:
        return None

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # Compute the change in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Calculate the distance using the Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance

def find_the_distance(start_address,end_address):


    
    start_coordinates = get_coordinates(start_address)
    end_coordinates = get_coordinates(end_address)

    if start_coordinates and end_coordinates:
        start_latitude, start_longitude = start_coordinates
        end_latitude, end_longitude = end_coordinates

        distance = calculate_distance(start_latitude, start_longitude, end_latitude, end_longitude)
        # print(f"Distance between {start_address} and {end_address}: {distance:.2f} kilometers")
        return int(distance)
    else:
        f"Failed to retrieve coordinates for start or end location."



