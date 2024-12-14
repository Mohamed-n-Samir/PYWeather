import openrouteservice
import folium
from tkinter import messagebox
import requests

class DirectionRoutes:
    
    def __init__(self, start_coords, end_coords, end_city):
        
        self.latitude = self.longitude = None
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.end_city = end_city
        
        self.client = openrouteservice.Client(key='5b3ce3597851110001cf6248b63de71a6f3c47ec8a4704d81931f5a7')
        
        try:
            response = requests.get('https://ipinfo.io/json')
        except requests.exceptions.ConnectTimeout:
            messagebox.showwarning(title="ConnectTimeout", message="Please Change your poor Internet Connection!😂")
            
        except requests.exceptions.ConnectionError:
            messagebox.showwarning(title="ConnectionError", message="Please Connect to Internet Connection!")
            
            
        # Check if the response is valid
        if response.status_code == 200:
            data = response.json()
            location = data['loc'] 
            # city = data['city'] 
            # country = data['country']
            
            self.latitude, self.longitude = location.split(',')
            
        else:
            messagebox.showerror( title="404" ,message="Unable to get Your Location location data!!")
   
    def get_distance_and_route(self):
        
        try:
            start_coords = (self.longitude, self.latitude)  
            end_coords = (self.start_coords, self.end_coords)     

            route = self.client.directions(
                coordinates=[start_coords, end_coords],
                profile='driving-car',
                format='geojson'
            )
        
        except Exception as e:
            messagebox.showwarning(title="Can't Drive to there", message="There's no way you can go there with driving!!")

        distance = route['features'][0]['properties']['segments'][0]['distance']
        if messagebox.askyesno(title="Direction and Distance", message=f"Distance between you and the Center of {self.end_city}: {distance / 1000} km\nAre you sure you want to download the\nroute map in HTML??"):

            m = folium.Map(location=list(reversed(start_coords)), tiles="cartodbpositron", zoom_start=5)

            route_coordinates = route['features'][0]['geometry']['coordinates']
            folium.PolyLine(locations=[list(reversed(coord)) for coord in route_coordinates], color="blue", weight=5).add_to(m)

            map_html = "./route_map.html"
            m.save(map_html)