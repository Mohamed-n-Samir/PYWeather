from tkinter import Tk, Frame, Button, Label, messagebox
from PIL import ImageTk, Image

from utils.VerticalScrolledFrame import VerticalScrolledFrame
from utils.SearchableComboBox import SearchableComboBox
from utils.CitiesFrame import CitiesFrame
from utils.SettingPopup import SettingPopup
from utils.InfoPopup import InfoPopup
from utils.WeatherPopup import WeatherApp

from Classes.Root import RootSingleton

import utils.Macros as Macros

from threading import Thread


class App(Tk):

    # --------------------------------------------| GlobalVars |--------------------------------------------
    
    choose_country_dropdown = choose_city_dropdown = settings = infos = None
    root = RootSingleton()

    def __init__(self):
        
        # --------------------------------------------| Root |--------------------------------------------
        super().__init__(className="Python Weather")
        self.title("PY Weather")
        self.geometry(Macros.WINDOW_GEOMETRY)
        self.wm_iconbitmap(self.root.ICON)
        self.configure(bg=Macros.APP_BG)
        
        
        # --------------------------------------------| Layout Main-Frame |--------------------------------------------
        self.main_frame = VerticalScrolledFrame(self, bg=Macros.APP_BG)
        self.main_frame.pack(fill="both", expand=1)


        # --------------------------------------------| Nav_Options Frame |--------------------------------------------
        self.nbar_frame = Frame(self.main_frame.interior, bg=Macros.GRAY)
        self.nbar_frame.pack(anchor="n", side="top", fill="x", pady=10, padx=10)
        

        # --------------------------------------------| Settings Button |--------------------------------------------
        self.settings_img = ImageTk.PhotoImage(
            Image.open(
                "./assets/settings.png"
            ).resize((25, 26))
        )
        self.settings_button = Button(
            self.nbar_frame,
            image=self.settings_img,
            relief="flat",
            overrelief="solid",
            bg=Macros.GRAY,
            command=self.handle_settings_popup,
        )
        self.settings_button.pack(anchor="e", side="right", padx=(4, 0))
        

        # --------------------------------------------| Info Button |--------------------------------------------
        self.info_img = ImageTk.PhotoImage(
            Image.open(
                "./assets/info.png"
            ).resize((30, 30))
        )
        self.info_button = Button(
            self.nbar_frame,
            image=self.info_img,
            relief="flat",
            overrelief="solid",
            bg=Macros.GRAY,
            command=self.handle_info_popup,
        )
        self.info_button.pack(anchor="e", side="right")
        
        
        # --------------------------------------------| Top Header |--------------------------------------------
        self.top_header = Frame(
            self.main_frame.interior,
            bg=Macros.APP_BG,
        )
        self.top_header.pack(pady=(0, 20))


        # --------------------------------------------| Program Title |--------------------------------------------
        Label(
            self.top_header,
            text="Python Weather",
            font=Macros.HEADER_FONT,
            bg=Macros.APP_BG,
            fg=Macros.GOLD,
        ).grid(row=0, column=0)

        
        # --------------------------------------------| Choose_Country Button |--------------------------------------------
        self.choose_btn = Button(
            self.main_frame.interior,
            text="Choose Cities",
            font=Macros.BUTTON_FONT,
            bg=Macros.BUTTON_BG,
            fg=Macros.BUTTON_FG,
            width=25,
            command=lambda: self.choose_country_popup(list(self.root.country_dict.keys())),
        )

        self.choose_btn.pack()
        
        
        # --------------------------------------------| Cities_List Frame |--------------------------------------------
        self.cities_frame = CitiesFrame(self.main_frame.interior)
        self.cities_frame.pack(pady=Macros.PADY)
        
        self.body_image = ImageTk.PhotoImage(
            Image.open(
                "./assets/weather-icon.png"
            ).resize((250,250))
        )
        
        
        # --------------------------------------------| Body Image |--------------------------------------------
        self.main_body_image = Label(self.main_frame.interior, image=self.body_image, bg=Macros.APP_BG)
        self.main_body_image.pack(pady=20)
        

        # --------------------------------------------| Fetch_Data Button |--------------------------------------------
        self.fetch_data_btn = Button(
            self.main_frame.interior,
            text="Fetch Country Data",
            font=Macros.LABEL_FONT,
            bg=Macros.GOLD,
            fg=Macros.BUTTON_BG,
            
            width=30,
            command=self.Fetch_data_with_threads,
        )

        self.fetch_data_btn.pack(pady=(0,30))
        
        
        # --------------------------------------------| Binding |--------------------------------------------
        
        self.bind_all("<Control-i>", lambda e: self.settings_button.invoke())
        self.bind_all("<Control-I>", lambda e: self.settings_button.invoke())

        self.bind_all("<F9>", lambda e: self.info_button.invoke())
        
        # --------------------------------------------| Initial Run |--------------------------------------------
        if self.root.default_city:
            self.cities_frame.add_label(self.root.default_city)



    # --------------------------------------------| Main Functions |--------------------------------------------
    
    """--------------------| Choose Country |--------------------
        Generates a popup with with country search and list
        of countries from the DB to choose from. On selection 
        it generates another popup to choose Wanted Cities From."""
    def choose_country_popup(self, options):
        self.choose_btn.config(state="disabled")
        self.choose_country_dropdown = SearchableComboBox(
            self,
            "Select Country...",
            options,
            on_close=lambda: close_popup(),
            after_select=lambda country: handle_selected_country(country),
        )

        def handle_selected_country(selected_country):
            country_code = self.get_country_code_from_dict(
                selected_country, self.root.country_dict
            )
            cities = self.get_cities(country_code)
            self.choose_city_popup(options=cities)

        def close_popup():
            self.choose_btn.config(
                state="normal",
            )
            self.choose_country_dropdown.destroy()
            
            
    """--------------------| Choose City |--------------------
        Generates a popup with city search and list
        of cities for the selected country from the DB 
        to choose from. On selection it add the city
        to the list which will be fetch."""
    def choose_city_popup(self, options):
        if self.choose_city_dropdown == None:
            self.choose_city_dropdown = SearchableComboBox(
                self,
                "Select City...",
                options,
                on_close=lambda: close_popup(),
                after_select=lambda text: self.cities_frame.add_label(text),
            )
        else:
            self.choose_city_dropdown.update_options(options)

        def close_popup():
            self.choose_city_dropdown.destroy()
            self.choose_city_dropdown = None


    """--------------------| Get Cities With Country Code |--------------------
        Return all cities that have the same country code."""
    def get_cities(self, country_code):
        cities = (self.root.CITIES[self.root.CITIES["country"] == country_code])["name"].to_list()
        return cities


    """--------------------| Get Country Code With Country name |--------------------
        Return The Country Code for the selected Country."""
    def get_country_code_from_dict(self, country_name: str, country_dict: dict) -> str:
        return country_dict.get(country_name, f"Country '{country_name}' not found.")


    """--------------------| Setting Popup Handler |--------------------
        Generate Settings popup and make sure that there's only one 
        instance of the setting popup."""
    def handle_settings_popup(self):
        if (
            not hasattr(self.settings, "winfo_exists")
            or not self.settings.winfo_exists()
            or self.settings == None
        ):
            self.settings = SettingPopup(self)

        else:
            self.settings.deiconify()
            self.settings.lift()


    """--------------------| Info Popup Handler |--------------------
        Generate Settings popup and make sure that there's only one 
        instance of the Info popup."""
    def handle_info_popup(self):
        if (
            not hasattr(self.infos, "winfo_exists")
            or not self.infos.winfo_exists()
            or self.infos == None
        ):
            self.infos = InfoPopup(self)

        else:
            # Focus the Toplevel window by bringing it to the front
            self.infos.deiconify()  # Make sure it's visible if it was hidden
            self.infos.lift()  # Bring the window to the front (focus)


    """--------------------| Fetch Cities Data From The api Using Threads |--------------------
        Checks if There's api Token or not if exists it checks if there's any selected cities
        then for each city it found it makes a new popup for that city with a unique thread to fetch
        it data then display it in the popup."""
    def Fetch_data_with_threads(self):
        if self.root.default_api_token == None or len(self.root.default_api_token) != 32:
            messagebox.showwarning(
                "No API Token",
                "Please Don't Forget to provide you api token\nfrom open weather in the Settings!!",
            )
            return

        cities = self.cities_frame.get_cities()
        if len(cities) > 0:
            for city in cities:
                if city in self.root.city_popups:
                    self.root.city_popups[city].lift()

                    continue

                weather_popup = WeatherApp(self, city)
                popup_thread = Thread(target=weather_popup.CW_Frame, name=city)
                self.root.city_popups[city] = weather_popup
                popup_thread.daemon = True
                popup_thread.start()
        else:
            messagebox.showwarning(
                "No Cities Provided",
                "Please Don't Forget to provide the List of cities\nto Fetch it's Data!!",
            )


if __name__ == "__main__":

    app = App()
    app.mainloop()
