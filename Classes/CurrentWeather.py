import countryinfo, datetime, pytz, requests

from Classes.Root import RootSingleton


# CLASS ------------------------------------------------------


class CurrentWeather:

    """-----------------------| Current Weather a Class to handle the openweather api requests |-----------------------
        fetching data from the open weather api and Formate the fetched data to be easier to handle and easy to use  
    """
    def __init__(self, city):
        
        self.root = RootSingleton()

        if not self.root.default_api_token or not self.root.UNITS or not self.root.default_unit:
            raise ValueError(
                "Class cannot be instantiated due to Wrong or Missing Value\nin API Token | Units | default unit"
            )
            
        self._city = city
        

    """-----------------------| Fetching city data |-----------------------
        fetching data from the api and storing the json data  
    """
    def get_weather(self) -> int:
        self.__current = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={self._city}&appid={self.root.default_api_token}&units={self.root.UNITS[self.root.default_unit][1]}",
            timeout=15,
        )

        # ------------| converting current weather in json format |------------
        self.__current_json = self.__current.json()
        self._lat = self.__current_json["coord"]["lat"]  # Latitude
        self._lon = self.__current_json["coord"]["lon"]  # Longitude



    """---------------------------| Current Temperature |--------------------------
        Fetch following details from current weather and return formatted tuple form
        return:
            temperature
            feels like
            name of temperature
            description of temperature
            humidity
            visibility  
    """
    def current_weather(self) -> tuple[int | float | str]:


        __temp = self.__current_json["main"]["temp"]
        __feels = self.__current_json["main"]["feels_like"]
        __temp_name = self.__current_json["weather"][0]["main"]
        __temp_des = self.__current_json["weather"][0][
            "description"
        ] 
        __humidity = self.__current_json["main"]["humidity"] 
        __visible = self.__current_json["visibility"]

        return (__temp, __feels, __temp_name, __temp_des, __humidity, __visible)


    """ ----------------------------| Location of City |----------------------------
        Fetch information of user's provided location and return formatted tuple form
        return:
            Latitude
            Longitude
            City name (official)
            Country code
            Country name
            Region of country
            Time Zone
            name of Time Zone
    """
    def location_details(self) -> tuple[float | str]:

        __city_name = self.__current_json["name"] 
        __con_code = self.__current_json["sys"]["country"]
        __country_name = pytz.country_names[__con_code]

        __country_info = countryinfo.CountryInfo(__country_name).info()
        __region = __country_info["region"]

        self.__zone_name = pytz.country_timezones[__con_code][0]
        __time_zone = datetime.datetime.now(
            tz=pytz.timezone(self.__zone_name)
        ).strftime("%z")

        return (
            self._lat,
            self._lon,
            __city_name,
            __con_code,
            __country_name,
            __region,
            __time_zone,
            self.__zone_name,
        )


    """ ----------------------------| Current Time of the Provided City |----------------------------
        Fetch current time and current day of user's choosed location
        return:
            Current Time
            Current Day
    """
    def current_time(self) -> tuple[str]:

        __current_time = datetime.datetime.now(
            pytz.timezone(self.location_details()[-1])
        ).strftime("%I:%M %p")
        __current_day = datetime.datetime.now(
            pytz.timezone(self.location_details()[-1])
        ).strftime("%a, %d %b' %y")

        return (__current_time, __current_day)


    """ ---------------------------------| Current Day Min Max Temperature |------------------------------
        Get minimum and maximum temperature of current day
        return:
            Minimum temperature
            Maximum temperature
    """
    def today_min_max_temp(self) -> tuple[float]:

        __min_temp = self.__current_json["main"]["temp_min"]
        __max_temp = self.__current_json["main"]["temp_max"]
        return (__min_temp, __max_temp)


    """ ------------------------------------| Sunrise and Sunset |----------------------------------------
        Get sunrise and sunset time of current day
        return:
            Sunrise
            Sunset
    """
    def current_sun_time(self) -> tuple[str]:

        __sunrise = datetime.datetime.fromtimestamp(
            self.__current_json["sys"]["sunrise"]
        ).strftime("%I:%M %p")
        __sunset = datetime.datetime.fromtimestamp(
            self.__current_json["sys"]["sunset"]
        ).strftime("%I:%M %p")
        return (__sunrise, __sunset)


    """ ------------------------------------| Wind Speed |----------------------------------------
        Get Wind speed of the current day
        return:
            wind speed
    """
    def get_wind_data(self):

        wind_speed = self.__current_json["wind"]["speed"]

        return wind_speed
    
    
    """ ------------------------------------| Pressure |----------------------------------------
        Get Air Pressure of the current day
        return:
            Pressure
    """
    def get_current_pressure(self):
        return f"{self.__current_json['main']['pressure']} hPa"
    
    
    """--------------------------| Current Weather Details |--------------------------
        It will make a Dictionary which holds, all values required in 
        current temperature details.
        Image path, Image pady, Frame ipadx, Image size, bg color, etc....
    """
    def current_weather_details(self) -> dict[str, int | float | str]:
        (
            current_temp,
            current_feels,
            current_temp_name,
            current_temp_des,
            current_humid,
            current_visibility,
        ) = self.current_weather()

        today_min, today_max = self.today_min_max_temp()
        current_time, current_date = self.current_time()

        _, _, current_city, _, current_country, current_region, current_time_zone, _ = (
            self.location_details()
        )

        current_sunrise, current_sunset = self.current_sun_time()
        current_wind_speed = self.get_wind_data()

        current_pressure = self.get_current_pressure()

        for i in self.root.weather_images:
            if (current_temp_name in self.root.weather_images[i]) and (
                current_temp_des in self.root.weather_images[i]
            ):
                current_image = i

                break
        raw_path = current_image.split("/")

        if (
            datetime.datetime.strptime(current_sunrise, "%I:%M %p")
            <= datetime.datetime.strptime(current_time, "%I:%M %p")
            <= datetime.datetime.strptime(current_sunset, "%I:%M %p")
        ):
            raw_path.insert(2, "day")
            self.bg_img = self.root.images_config[current_image][2][0]
            self.fg_img = self.root.images_config[current_image][2][1]
        else:
            raw_path.insert(2, "night")
            self.bg_img = self.root.images_config[current_image][3][0]
            self.fg_img = self.root.images_config[current_image][3][1]

        current_exact_image = "/".join(raw_path)

        current_details = {
            "Image": current_exact_image,
            "bg color": self.bg_img,
            "light color": self.fg_img,
            "Image size": self.root.images_config[current_image][1][0],
            "ipadx": self.root.images_config[current_image][0][0][0],
            "ipady": self.root.images_config[current_image][0][0][1],
            "Temp": current_temp,
            "Feels": current_feels,
            "Name": current_temp_name,
            "Humidity": current_humid,
            "Visibility": current_visibility,
            "Min": today_min,
            "Max": today_max,
            "Time": current_time,
            "Date": current_date,
            "City": current_city,
            "Country": current_country,
            "Region": current_region,
            "Time zone": current_time_zone,
            "Sunrise": current_sunrise,
            "Sunset": current_sunset,
            "WindSpeed": f"{current_wind_speed} m/s",
            "pressure": current_pressure,
        }
        return current_details