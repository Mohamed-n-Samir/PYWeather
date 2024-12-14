import pandas as pd


class RootSingleton:
    _instance = default_unit = default_api_token = default_city = None
    city_popups = {}

    # CONSTS ------------------------------------------------------------------------------------------------------------------------------------------------------
    COUNTRIES = pd.read_csv("./data/sorted_countries.csv")[
        ["Country Name", "Country Code"]
    ]
    CITIES = pd.read_json("./data/city_list.json")

    ICON = "./assets/weather_app_logo.ico"

    UNITS = {
        "C": ["Celsius", "metric"],
        "F": ["Fahreneit", "imperial"],
    }

    country_dict = dict(zip(COUNTRIES["Country Name"], COUNTRIES["Country Code"]))

    images_config = {
        "./assets/sunny.png": (
            [(10, 0), (9, 0)],
            [(160, 160), (85, 80)],
            ["#F5B041", "#FFE082"],
            ["#55555D", "#929297"],
        ),
        "./assets/clear_sky.png": (
            [(10, 0), (10, 0)],
            [(160, 120), (80, 80)],
            ["#03A9F4", "#81D4FA"],
            ["#21618C", "#2980B9"],
        ),
        "./assets/cloudy.png": (
            [(15, 5), (8, 5)],
            [(130, 130), (90, 70)],
            ["#308DA5", "#87ceeb"],
            ["#308DA5", "#87ceeb"],
        ),
        "./assets/foggy.png": (
            [(5, 10), (10, 5)],
            [(170, 110), (110, 70)],
            ["#48C9B0", "#A3E4D7"],
            ["#E3915C", "#EDBB99"],
        ),
        "./assets/snow.png": (
            [(15, 5), (13, 0)],
            [(160, 140), (90, 80)],
            ["#00BCD4", "#80DEEA"],
            ["#00BCD4", "#80DEEA"],
        ),
        "./assets/windy.png": (
            [(0, 5), (10, 0)],
            [(160, 145), (100, 80)],
            ["#34495E", "#AEB6BF"],
            ["#34495E", "#AEB6BF"],
        ),
        "./assets/rainy.png": (
            [(15, 0), (8, 0)],
            [(160, 150), (80, 80)],
            ["#1976D2", "#64B5F6"],
            ["#1976D2", "#64B5F6"],
        ),
        "./assets/thunderstorm.png": (
            [(0, 0), (0, 1)],
            [(160, 150), (100, 80)],
            ["#2980B9", "#7FB3D5"],
            ["#2980B9", "#7FB3D5"],
        ),
    }

    weather_images = {
        "./assets/sunny.png": ["Clear", "clear sky"],
        "./assets/clear_sky.png": ["Clouds", "few clouds"],
        "./assets/cloudy.png": [
            "Clouds",
            "scattered clouds",
            "broken clouds",
            "overcast clouds",
        ],
        "./assets/foggy.png": [
            "Mist",
            "Smoke",
            "smoke",
            "Haze",
            "haze",
            "Fog",
            "mist",
            "fog",
        ],
        "./assets/snow.png": [
            "Snow",
            "freezing rain",
            "light snow",
            "Heavy snow",
            "Steet",
            "Light shower sleet",
            "Shower sleet",
            "Light rain and snow",
            "Rain and snow",
            "Light shower snow",
            "Shower snow",
            "Heavy shower snow",
            "rain and snow",
        ],
        "./assets/windy.png": [
            "Dust",
            "sand/ dust whirls",
            "Sand",
            "sand",
            "dust",
            "Ash",
            "Squall",
            "squalls",
            "Tornado",
            "tornado",
        ],
        "./assets/rainy.png": [
            "Drizzle",
            "light intensity drizzle",
            "drizzle",
            "heavy intensity drizzle",
            "light intensity drizzle rain",
            "drizzle rain",
            "heavy intensity drizzle rain",
            "shower rain and drizzle",
            "heavy shower rain and drizzle",
            "shower drizzle",
            "Rain",
            "light rain",
            "moderate rain",
            "heavy intensity rain",
            "very heavy rain",
            "extreme rain",
            "light intensity shower rain",
            "shower rain",
            "heavy intensity shower rain",
            "ragged shower rain",
        ],
        "./assets/thunderstorm.png": [
            "Thunderstorm",
            "thunderstorm with light rain",
            "thunderstorm with rain",
            "thunderstorm with heavy rain",
            "light thunderstorm",
            "thunderstorm",
            "thunderstorm",
            "heavy thunderstorm",
            "ragged thunderstorm",
            "thunderstorm with light drizzle",
            "thunderstorm with drizzle",
            "thunderstorm with heavy drizzle",
        ],
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init()

        return cls._instance

    def init(self):
        with open("./assets/api_token.txt") as file:
            token_value = file.read()
            if len(token_value) == 32:
                self.default_api_token = token_value
            else:
                print(
                    "The default Value of the Token must be 32 character length"
                )

        with open("./assets/location.txt") as file:
            loc_value = file.read()
            if loc_value in self.get_all_cities():
                self.default_city = loc_value
            else:
                print(
                    "The default Value of the city can't be Handled by the Api"
                )

        with open("./assets/unit.txt", "r+") as file:
            unit_value = file.read().strip()
            if unit_value in ["C", "F"]:
                self.default_unit = unit_value
            else:
                self.default_unit = "C"
                file.write("C")
                file.seek(0)
                print(
                    "The default Value of the Unit must be 'C' or 'F' only"
                )

    def get_all_cities(self):
        cities = self.CITIES["name"].to_list()
        return cities
