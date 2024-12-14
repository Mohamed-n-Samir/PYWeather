from tkinter import Toplevel, Label, Frame, Button, LabelFrame

from Classes.Root import RootSingleton

import utils.Macros as Macros

from PIL import Image, ImageTk


class InfoPopup(Toplevel):
    
    """--------------------------------------| Info Window |--------------------------------------
        Display Info window, in which all information of Weather App will show"""
    def __init__(self, parent):
        super().__init__(parent, bg=Macros.APP_BG)
        
        self.master = parent
        self.root = RootSingleton()
        
        # --------------------------------------| Info Window |--------------------------------------
        self.focus()
        self.title("Weather App - Info")
        self.geometry("500x600")
        self.transient(self.master)
        self.wm_iconbitmap(self.root.ICON)

        self.resizable(False, False)
        # --------------------------------------| Info Label |--------------------------------------
        self.info_label = Label(
            self,
            text="Info",
            font=("Tahoma", 18, "bold"),
            bg=Macros.APP_BG,
            justify="center",
        )
        self.info_label.pack(side="top", fill="x", pady=10)
        self.info_sep1 = Frame(self, bg="black")
        self.info_sep1.pack(side="top", fill="x", padx=10, pady=5)

        # --------------------------------------| Developer Label |--------------------------------------
        self.dev_detail = Label(
            self,
            text="This Application is developed by E-shik Dev and special Thanks\nto Parampreet Singh for the assets and the design Idea.",
            font=("Tahoma", 12),
            bg=Macros.APP_BG,
            padx=20,
            justify="left",
        )
        self.dev_detail.pack(side="top", anchor="nw")
        self.dev_github = Button(
            self,
            text="https://github.com/mohamed-n-samir",
            font=("Tahoma", 10),
            bg=Macros.APP_BG,
            fg="blue",
            activebackground=Macros.APP_BG,
            relief="flat",
            overrelief="flat",
            padx=20,
            # command=self.github_link,
        )
        self.dev_github.pack(side="top", anchor="nw")
        self.info_sep2 = Frame(self, bg="black")
        self.info_sep2.pack(side="top", fill="x", padx=10, pady=5)

        # --------------------------------------| WA details |--------------------------------------
        self.WA_details = LabelFrame(
            self,
            text="  Data Details",
            font=("Tahoma", 14, "bold"),
            bg=Macros.APP_BG,
            padx=30,
            pady=10,
            relief="flat",
        )
        # --------------------------| Starting |--------------------------
        self.wa_start = Label(
            self.WA_details,
            text="All weather data is being fetched from OpenWeathermap APIs:",
            font=("Tahoma", 12),
            bg=Macros.APP_BG,
            justify="left",
            padx=10,
        )
        self.wa_start.grid(row=0, column=0, columnspan=2, sticky="w")

        # --------------------------| Current Weather Data API button |--------------------------
        self.current_api_button = Button(
            self.WA_details,
            text="• Current Weather Data API",
            font=("Tahoma", 12, "underline"),
            bg=Macros.APP_BG,
            activebackground=Macros.APP_BG,
            fg="blue",
            justify="left",
            relief="flat",
            overrelief="flat",
            padx=10,
            # command=self.current_api_link,
        )
        self.current_api_button.grid(row=1, column=0, sticky="w")

        # --------------------------| One Call API button |--------------------------
        self.one_call_api_button = Button(
            self.WA_details,
            text="• One Call API",
            font=("Tahoma", 12, "underline"),
            bg=Macros.APP_BG,
            activebackground=Macros.APP_BG,
            fg="blue",
            justify="left",
            relief="flat",
            overrelief="flat",
            padx=10,
            # command=self.one_call_api_link,
        )
        self.one_call_api_button.grid(row=2, column=0, sticky="w")

        # --------------------------| Open Weather map image button |--------------------------
        self.OW_img = ImageTk.PhotoImage(
            Image.open("./assets/open_weather_logo.png").resize((100, 40))
        )
        self.OW_logo = Button(
            self.WA_details,
            image=self.OW_img,
            bg=Macros.APP_BG,
            activebackground=Macros.APP_BG,
            relief="flat",
            overrelief="solid",
            padx=10,
            # command=self.open_weather_link,
        )
        self.OW_logo.grid(row=1, column=1, rowspan=2, sticky="w")
        self.OW_logo.bind(
            "<Enter>", lambda e: self.OW_logo.configure(bg=Macros.GOLD)
        )
        self.OW_logo.bind("<Leave>", lambda e: self.OW_logo.configure(bg=Macros.APP_BG))

        # --------------------------| Extra Details about App |--------------------------
        self.wa_extra = Label(
            self.WA_details,
            text="It display Current Weather details using MultiThreading each\nThread get the data of another Country\nand note that the free api token allow only for 60 request/min.\nso dont try to make more than 50 cities at a time\nthe Application Automatically Fetches data every min for each country\nPlease try to search weather after interval of 15 seconds to keep application stable.",
            font=("Tahoma", 12),
            bg=Macros.APP_BG,
            justify="left",
            padx=10,
            wraplength=450,
        )
        self.wa_extra.grid(row=3, column=0, columnspan=2, sticky="w", pady=10)

        self.WA_details.pack(side="top", fill="x", pady=10)
        self.info_sep3 = Frame(self, bg="black")
        self.info_sep3.pack(side="top", fill="x", padx=10)

        # --------------------------------------| Shortcut Keys |--------------------------------------
        self.Shortcut_keys = LabelFrame(
            self,
            text="  Shortcut Keys",
            font=("Tahoma", 14, "bold"),
            bg=Macros.APP_BG,
            padx=30,
            pady=10,
            relief="flat",
        )
        # ----------| Info Label |----------
        self.info_label = Label(
            self.Shortcut_keys,
            text="Info",
            font=("Tahoma", 12),
            bg=Macros.APP_BG,
            justify="left",
            padx=10,
        )
        self.info_label.grid(row=0, column=0, sticky="e", pady=5)

        # ----------| Info key |----------
        self.info_key = Label(
            self.Shortcut_keys,
            text="F9",
            font=("Tahoma", 12),
            bg=Macros.GOLD,
            justify="left",
            padx=10,
        )
        self.info_key.grid(row=0, column=1, sticky="nswe", pady=5)
        self.info_side_sep = Frame(self.Shortcut_keys, bg=Macros.APP_BG)
        self.info_side_sep.grid(row=0, column=2, rowspan=2, ipadx=20)

        # ----------| Settings Label |----------
        self.settings_label = Label(
            self.Shortcut_keys,
            text="Settings",
            font=("Tahoma", 12),
            bg=Macros.APP_BG,
            justify="left",
            padx=10,
        )
        self.settings_label.grid(row=0, column=3, sticky="e", pady=5)

        # ----------| Settings Key |----------
        self.settings_key = Label(
            self.Shortcut_keys,
            text="Control + i",
            font=("Tahoma", 12),
            bg=Macros.GOLD,
            justify="left",
            padx=10,
        )
        self.settings_key.grid(row=0, column=4, sticky="nswe", pady=5)
        self.Shortcut_keys.pack(side="top", fill="x", pady=10)
