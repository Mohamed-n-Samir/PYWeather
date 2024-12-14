import requests, datetime
from Classes.CurrentWeather import CurrentWeather

class Forecast5Days(CurrentWeather):
    

    """--------------------------------------| Five Days Forecasting Data  |--------------------------------------
        Fetch forecast from Forcast API and other details of provided city for the next five Days.
    """
    def __init__(self, city):
          super().__init__(city)
          
    """-----------------------| Fetching Next 5 Days city data |-----------------------
        fetching data from the api and storing the json data  
    """
    def get_forecast(self):

            self.__forecast = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={self._city}&appid={self.root.default_api_token}&units={self.root.UNITS[self.root.default_unit][1]}&exclude=minutely", timeout=15)

            self._five_days_weather = self.__forecast.json()
            
            
            
    """-----------------------| Formatting Days city data |-----------------------
        Get information of next 5 days each day info is stored in a dictionary manner
        {   "Date" : date,
            "Temp" : temp,         
            "Day:" : day_temp, 
            "Night:" : night_temp,
            "Name" : weather_name,
            "Description" : weather_des
        }

    """
    def five_days_forecast(self) -> list[dict[str, int | float | str]]:

        __five_days_temps = []
        for __day in self._five_days_weather["list"]:

            __date = datetime.datetime.fromtimestamp(__day["dt"]).strftime("%d %b' %y")
            __temp = round(__day['main']["temp"], 2)
            __max_temp = round(__day['main']["temp_max"], 2)
            __min_temp = round(__day['main']["temp_min"], 2)
            __weather_name = __day["weather"][0]["main"]
            __weather_des = __day["weather"][0]["description"]

            __day_set = {"Date" : __date, "Temp" : __temp, "Day:" : __max_temp,
            "Night:" : __min_temp, "Name" : __weather_name, "Description" : __weather_des}
            
            __five_days_temps.append(__day_set)
        
        return __five_days_temps
    
    
    """--------------------------| Five Days Weather Forecast Details |--------------------------
        It will make a list of dictionaries which holds, all values in five_days_forecast() return dict
        as well as some extra things:
        Image path, Image pady, Frame ipadx, Image size, bg color
    """
    def forecast_details(self) -> list[dict[str, int | float | str]]:

        forecast = self.five_days_forecast()
        raw_Wdetails = []
        
        date_now = self.current_time()[1].split(", ")[1]
        
        for i, day in enumerate(forecast):

            if date_now == day['Date']:
                continue
            
            date_now = day['Date']
            
            #-----| Getting image according to weather |-----
            for image, group in self.root.weather_images.items():
                if (day["Name"] and day["Description"] in group):
                    raw_path = image.split('/')
                    img_path = "./" + raw_path[1] + "/day/" + raw_path[-1]
                    break
                        
            Ipady = self.root.images_config[image][0][1][1]
            Fipadx = self.root.images_config[image][0][1][0]
            size = self.root.images_config[image][1][1]
            color = self.bg_img
            light_color = self.fg_img

            details = {**day, "Image" : img_path, "Image pady" : Ipady, "Frame ipadx" : Fipadx, "Image size" : size, "bg color" : color, "light color": light_color}
            if not i:
                details["Date"] = "Tomorrow"
            
            raw_Wdetails.append(details)

        return raw_Wdetails
