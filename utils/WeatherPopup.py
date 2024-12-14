from tkinter import Toplevel, Label, Frame, Button, LabelFrame, messagebox
from PIL import Image, ImageTk
from Classes.Forecast5Days import Forecast5Days
from Classes.DirectionRoutes import DirectionRoutes 
from threading import Thread, Event, Lock
from time import sleep, time

import utils.Macros as Macros
from utils.ForecastPopup import ForecastPopup

import datetime, requests, pytz


class WeatherApp(Toplevel, Forecast5Days):
    
    """--------------------------------------| City Data popup |--------------------------------------
        Display City Data Popup, in which user can See:
        1. Temp Description.
        2. Temp Degree.
        3. Temp Feels Like.
        4. Temp min.
        5. Temp max.
        6. Sunrise time.
        7. Sunset time.
        8. Time.
        9. Date.
        10. Wind Speed.
        11. Pressure.
        12. Visibility.
        13. Humidity.
        14. city origin.
        15. More data (ForecastPopup) go to ForecastPopup in Classes 4 more details.
        16. calculating traveling distance and downloading the route map 
    """
    def __init__(self, parent, city):
        super().__init__(parent, bg="cyan")
        Forecast5Days.__init__(self, city)
        
        self.city = city
        self.master = parent
        self.title(f"{self.city} Weather Thread")
        self.wm_iconbitmap(self.root.ICON)

        self.width = 680
        self.height = 420
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False,False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.on_close())
        
        
        # ------------------------| Events to Make Sure than no race conditions and no functions still working on closing the popup |------------------------
        self.stop_threads_event = Event()
        self.stop_thread_1_event = Event()
        self.stop_thread_2_event = Event()
        self.thread_lock = Lock()

        # ----------| Current Weather Frame |----------
        self.current_stats = Frame(self, bg="cyan")
        self.current_stats.pack(anchor="nw", side="left", fill="both", expand=1)

        self.temp = Label(
            self,
            text="Loading...",
            font=("Tahoma", 18, "bold"),
            justify="center",
            bg="cyan",
        )
        self.temp.pack(side="left", fill="both", ipadx=self.width // 2)


    def CW_Frame(self) -> None:
        """--------------------------| Current Weather Frame |--------------------------
        Make Current Weather Frame which includes:
        current weather image, weather, time, timezone, location, date, min, max, humidity
        """
        
        try:
            self.get_weather()
                
        except requests.exceptions.ConnectionError:
            self.temp.config(text="Connection Error!!\nPlease Connect to the Internet")
            return
        except requests.Timeout:  # response time out
            self.temp.config(text="response time out\nTry again Later!!!")
            return
        except KeyError:
            self.temp.config(text="City name is not present!!")
            return
        
        self.temp.destroy()
        self.CW = self.current_weather_details()
        self.current_stats.configure(bg=self.CW["bg color"])

        self.CWFrame = Frame(self.current_stats, bg=self.CW["bg color"])

        # --------------------------| Current Weather main Frame |--------------------------
        self.CW_main = Frame(self.CWFrame, bg=self.CW["bg color"], pady=5)

        # ---------------| Current Weather Image Frame |---------------
        self.cw_img_frame = LabelFrame(
            self.CW_main,
            text=self.CW["Name"],
            font=("Tahoma", 24),
            labelanchor="s",
            relief="flat",
            bg=self.CW["bg color"],
        )

        # -----| Image |-----
        self.CImg = ImageTk.PhotoImage(
            Image.open(self.CW["Image"]).resize(self.CW["Image size"])
        )
        self.cw_img = Label(
            master=self.cw_img_frame, image=self.CImg, bg=self.CW["bg color"]
        )
        self.cw_img.pack()

        self.cw_img_frame.pack(
            anchor="nw", side="left", ipadx=self.CW["ipadx"], ipady=self.CW["ipady"]
        )

        # ---------------| Current Weather details Frame |---------------
        self.cwd_frame = Frame(self.CW_main, bg=self.CW["bg color"])
        # -----| Temperature |-----
        if (self.CW["Temp"] < 0) and (len(str(self.CW["Temp"])) == 5):
            self.ctemp = f' -{str(self.CW["Temp"])[1:]}°{self.root.default_unit.lower()}'

        elif len(str(self.CW["Temp"])) == 4:
            self.ctemp = f' {str(self.CW["Temp"])}°{self.root.default_unit.lower()}'

        else:
            self.ctemp = f' {str(self.CW["Temp"])}°{self.root.default_unit.lower()}'

        self.CTemp = Label(
            self.cwd_frame, text=self.ctemp, font=("Tahoma", 50), bg=self.CW["bg color"]
        )
        self.CTemp.grid(row=0, column=0, rowspan=3, sticky="se", padx=(0, 15))

        # -----| Time |-----
        self.CTime = Label(
            self.cwd_frame,
            text=f'{self.CW["Time"]:^11}',
            font=("Tahoma", 30),
            bg=self.CW["bg color"],
            anchor="s"
        )
        self.CTime.grid(row=1, column=3, sticky="s", ipadx=5)

        # -----| Date |-----
        self.CDate = Label(
            self.cwd_frame,
            text=f'{self.CW["Date"]:^16}',
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
            anchor="s"
        )
        self.CDate.grid(row=3, column=3, sticky="n")

        # -----| Feel Like |-----
        self.Cfeels = Label(
            self.cwd_frame,
            text=f"Feels like:{self.CW['Feels']:>10}°{self.root.default_unit.lower()}",
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
        )
        self.Cfeels.grid(row=3, column=0, columnspan=2, sticky="nswe", padx=(10,0))

        # -----| Minimum |-----
        self.CMin = Label(
            self.cwd_frame,
            text=f"Min:\t{self.CW['Min']:>10}°{self.root.default_unit.lower()}",
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
        )
        self.CMin.grid(row=4, column=0, columnspan=2, sticky="nswe", padx=(10,0))

        # -----| Maximum |-----
        self.CMax = Label(
            self.cwd_frame,
            text=f"Max:\t{self.CW['Max']:>10}°{self.root.default_unit.lower()}",
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
        )
        self.CMax.grid(row=5, column=0, columnspan=2, sticky="nswe", padx=(10,0))

        # -----| Time Zone |-----
        self.CTZone = Label(
            self.cwd_frame,
            text=f"GMT {self.CW['Time zone'][:-2] + ':' + self.CW['Time zone'][-2:]}",
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
        )

        # -----| City |-----
        self.CCity = Label(
            self.cwd_frame,
            text=f'{self.CW["City"]:^20}',
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
        )

        # -----| Country, Continent |-----
        if (" " in self.CW["Country"]) or (len(self.CW["Country"]) >= 10):
            self.con = self.CW["Country"]
        else:
            self.con = self.CW["Country"] + ", " + self.CW["Region"]

        self.CCon = Label(
            self.cwd_frame,
            text=f"{self.con:^20}",
            font=("Tahoma", 18),
            bg=self.CW["bg color"],
        )

        self.CCity.grid(row=4, column=3, sticky="nswe")
        self.CCon.grid(row=5, column=3, sticky="nswe")

        self.cwd_frame.pack(anchor="nw", side="left")
        self.CW_main.pack(side="top", ipadx=10)
        self.cw_sep = Frame(self.CWFrame, bg="black")
        self.cw_sep.pack(side="top", fill="x", pady=5)

        # --------------------------| Current Weather more Frame |--------------------------
        self.CW_more = Frame(self.CWFrame, bg=self.CW["bg color"])

        # --------------------| Sunrise |--------------------
        self.CSR = Label(
            self.CW_more,
            text="Sunrise",
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CSR.grid(row=0, column=0, sticky="nesw")
        self.CSR_img = ImageTk.PhotoImage(
            Image.open("./assets/sunrise.png").resize((30, 30))
        )
        self.CSR_logo = Label(self.CW_more, image=self.CSR_img, bg=self.CW["bg color"])
        self.CSR_logo.grid(row=0, column=1, sticky="nesw")
        self.CSR_time = Label(
            self.CW_more,
            text=f': {self.CW["Sunrise"].lower()}',
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CSR_time.grid(row=0, column=2, sticky="nesw", padx=(0,20))

        # --------------------| Sunset |--------------------
        self.CSS = Label(
            self.CW_more,
            text="Sunset",
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CSS.grid(row=0, column=3, sticky="nesw", padx=(20,0))
        self.CSS_img = ImageTk.PhotoImage(
            Image.open("./assets/sunset.png").resize((35, 25))
        )
        self.CSS_logo = Label(self.CW_more, image=self.CSS_img, bg=self.CW["bg color"])
        self.CSS_logo.grid(row=0, column=4, sticky="nesw")
        self.CSS_time = Label(
            self.CW_more,
            text=f': {self.CW["Sunset"].lower()}',
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CSS_time.grid(row=0, column=5, sticky="nesw")

        # --------------------| WindSpeed |--------------------
        self.CMR = Label(
            self.CW_more,
            text="WindSpeed",
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CMR.grid(row=1, column=0, sticky="nesw")
        self.CMR_img = ImageTk.PhotoImage(
            Image.open("./assets/day/windy.png").resize((30, 30))
        )
        self.CMR_logo = Label(self.CW_more, image=self.CMR_img, bg=self.CW["bg color"])
        self.CMR_logo.grid(row=1, column=1, sticky="nesw")
        self.CMR_time = Label(
            self.CW_more,
            text=f': {self.CW["WindSpeed"]}',
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CMR_time.grid(row=1, column=2, sticky="nesw",padx=(0,20))

        # --------------------| Pressure |--------------------
        self.CMS = Label(
            self.CW_more,
            text="Pressure",
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CMS.grid(row=1, column=3, sticky="nesw", padx=(20,0))
        self.CMS_img = ImageTk.PhotoImage(
            Image.open(f"./assets/pressure.png").resize((35, 35))
        )
        self.CMS_logo = Label(self.CW_more, image=self.CMS_img, bg=self.CW["bg color"])
        self.CMS_logo.grid(row=1, column=4, sticky="nesw")
        self.CMS_time = Label(
            self.CW_more,
            text=f': {self.CW["pressure"].lower()}',
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CMS_time.grid(row=1, column=5, sticky="nesw")

        # --------------------| Humidity |--------------------
        self.CHumid = Label(
            self.CW_more,
            text="Humidity",
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CHumid.grid(row=2, column=0, sticky="nesw")
        self.CHumid_img = ImageTk.PhotoImage(
            Image.open("./assets/humidity.png").resize((35, 25))
        )
        self.CHumidity_logo = Label(
            self.CW_more, image=self.CHumid_img, bg=self.CW["bg color"]
        )
        self.CHumidity_logo.grid(row=2, column=1, sticky="nesw")
        self.CHumid_mark = Label(
            self.CW_more,
            text=f': {self.CW["Humidity"]}%',
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CHumid_mark.grid(row=2, column=2, sticky="nesw", padx=(0,20))

        # --------------------| Weather Type Detail |--------------------
        self.CVisible = Label(
            self.CW_more,
            text="Visibility",
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CVisible.grid(row=2, column=3, sticky="nesw", padx=(20,0))
        self.CVisible_img = ImageTk.PhotoImage(
            Image.open("./assets/visibility.png").resize((35, 25))
        )
        self.CVisible_logo = Label(
            self.CW_more, image=self.CVisible_img, bg=self.CW["bg color"]
        )
        self.CVisible_logo.grid(row=2, column=4, sticky="nesw")
        self.CVisible_mark = Label(
            self.CW_more,
            text=f': {self.CW["Visibility"]/1000} km',
            font=("Tahoma", 16),
            bg=self.CW["bg color"],
            anchor="w",
        )
        self.CVisible_mark.grid(row=2, column=5, sticky="nesw")

        self.CW_more.pack(anchor="s", side="bottom", pady=8)

        self.CWFrame.pack(expand=1, fill="both")
        
        self.show_more_frame = Frame(
            self.current_stats,
            bg=self.CW["bg color"],
        )
        
        self.show_more_frame.columnconfigure([0,1], weight=1)
        self.show_more_frame.pack(fill="both",anchor="s", side="bottom", pady=(15,20))
        
        self.show_more_button = Button(
            self.show_more_frame,
            text="Show More",
            width=20,
            font=Macros.LABEL_FONT,
            bg=self.CW["bg color"],
            command=self.show_more_details
        )
        
        self.show_more_button.grid(row=0, column=0, padx=(0,5), sticky="nes")
        
        self.direction_distance_button = Button(
            self.show_more_frame,
            text="Traveling Distance",
            width=20,
            font=Macros.LABEL_FONT,
            bg=self.CW["bg color"],
            command=self.show_traveling_distance_and_route
        )
        
        self.direction_distance_button.grid(row=0, column=1, padx=(5,0), sticky="nws")
        
        
        self.update()
        
        """---------------------| Thread Generation |---------------------
        Gen 2 Thread :
            1. update date & time each second.
            2. update all other information with api call.
        """
        self.date_time_thread = Thread(target=self.date_time_update)
        self.date_time_thread.daemon = True
        self.date_time_thread.start()
        
        self.update_all_thread = Thread(target=self.temp_update)
        self.update_all_thread.daemon = True
        self.update_all_thread.start()


    """-----------------------| date & time Update |-----------------------
        Updates the time and date after a second by requesting the pytz api.
        interrupting the thread on closing the popup
    """
    def date_time_update(self) -> None:
        while not self.stop_threads_event.is_set():
            try:
                self.new_time = datetime.datetime.now(pytz.timezone(self.location_details()[-1])).strftime("%I:%M %p")
                self.new_date = datetime.datetime.now(pytz.timezone(self.location_details()[-1])).strftime("%a, %d %b' %y")
                with self.thread_lock:
                    self.CTime.configure(text=f'{self.new_time:^11}')
                    self.CDate.configure(text=f'{self.new_date:^16}')
                
                sleep(1)
            except KeyError:
                print("exiting Thread Due to bad Network Connection!!")
                
        else:
            self.stop_thread_1_event.set()
       
            
    """-----------------------| Temperature Update |-----------------------
        Updates all data provided on the api and showed on the popup and
        updates the popup ui.
        interrupting the thread on closing the popup
    """
    def temp_update(self) -> None:
        
        """Updates all the values after 5 minutes."""
        while not self.stop_threads_event.is_set():
            start_time = time()
            while time() - start_time < 60:
                if self.stop_threads_event.is_set():
                    break
                sleep(1)
                
            else:self.update_values()
            
        else:
            self.stop_thread_2_event.set()
            
        
    def update_values(self) -> None:
        """Update all the values and colors in application according to searched city"""

        self.CW = self.current_weather_details()
        self.configure(bg=self.CW["bg color"])

        #--------------------------| Current Weather Frame values |--------------------------
        self.current_stats.configure(bg=self.CW["bg color"])
        self.CWFrame.configure(bg=self.CW["bg color"])
        self.CW_main.configure(bg=self.CW["bg color"])

        self.cw_img_frame.configure(text=self.CW["Name"], bg=self.CW["bg color"])
        self.CImg = ImageTk.PhotoImage(Image.open(self.CW["Image"]).resize(self.CW["Image size"]))
        self.cw_img.configure(image=self.CImg, bg=self.CW["bg color"])
        self.cw_img_frame.pack_configure(ipadx=self.CW["ipadx"], ipady=self.CW["ipady"])

        self.cwd_frame.configure(bg=self.CW["bg color"])

        if (self.CW["Temp"] < 0) and (len(str(self.CW["Temp"]))==5):
            self.ctemp = f' -{str(self.CW["Temp"])[1:]}°{self.root.default_unit.lower()}'

        elif (len(str(self.CW["Temp"]))==4):
            self.ctemp = f' {str(self.CW["Temp"])}°{self.root.default_unit.lower()}'

        else:   self.ctemp = f' {str(self.CW["Temp"])}°{self.root.default_unit.lower()}'

        self.CTemp.configure(text=self.ctemp, bg=self.CW["bg color"])
        
        with self.thread_lock:
            self.CTime.configure(text=f'{self.CW["Time"]:^11}', bg=self.CW["bg color"])
            self.CDate.configure(text=f'{self.CW["Date"]:^16}', bg=self.CW["bg color"])
            
        self.Cfeels.configure(text=f"Feels like:{self.CW['Feels']:>10}°{self.root.default_unit.lower()}", bg=self.CW["bg color"])
        self.CMin.configure(text=f"Min:\t{self.CW['Min']:>10}°{self.root.default_unit.lower()}", bg=self.CW["bg color"])
        self.CMax.configure(text=f"Max:\t{self.CW['Max']:>10}°{self.root.default_unit.lower()}", bg=self.CW["bg color"])
        self.CTZone.configure(text=f"GMT {self.CW['Time zone'][:-2] + ':' + self.CW['Time zone'][-2:]}", bg=self.CW["bg color"])
        self.CCity.configure(text=f'{self.CW["City"]:^20}', bg=self.CW["bg color"])

        if (" " in self.CW["Country"]) or (len(self.CW["Country"]) >= 10):
            self.con = self.CW["Country"]
        else:
            self.con = self.CW["Country"] + ", " + self.CW["Region"]
        self.CCon.configure(text=f"{self.con:^20}", bg=self.CW["bg color"])

        self.CW_more.configure(bg=self.CW["bg color"])

        self.CSR.configure(bg=self.CW["bg color"])
        self.CSR_logo.configure(bg=self.CW["bg color"])
        self.CSR_time.configure(text=f': {self.CW["Sunrise"].lower()}', bg=self.CW["bg color"])

        self.CSS.configure(bg=self.CW["bg color"])
        self.CSS_logo.configure(bg=self.CW["bg color"])
        self.CSS_time.configure(text=f': {self.CW["Sunset"].lower()}', bg=self.CW["bg color"])

        self.CMR.configure(bg=self.CW["bg color"])
        self.CMR_logo.configure(bg=self.CW["bg color"])
        self.CMR_time.configure(text=f': {self.CW["WindSpeed"]}', bg=self.CW["bg color"])

        self.CMS.configure(bg=self.CW["bg color"])
        self.CMS_logo.configure(bg=self.CW["bg color"])
        self.CMS_time.configure(text=f': {self.CW["pressure"].lower()}', bg=self.CW["bg color"])

        self.CHumid.configure(bg=self.CW["bg color"])
        self.CHumidity_logo.configure(bg=self.CW["bg color"])
        self.CHumid_mark.configure(text=f': {self.CW["Humidity"]}%', bg=self.CW["bg color"])

        self.CVisible.configure(bg=self.CW["bg color"])
        self.CVisible_logo.configure(bg=self.CW["bg color"])
        self.CVisible_mark.configure(text=f': {self.CW["Visibility"]/1000} km', bg=self.CW["bg color"])


    """-----------------------| Closing the Popup |-----------------------
        Make sure that no thread or function running before closing
        the popup.
    """
    def on_close(self):
        self.stop_threads_event.set()   
            
        thread = Thread(target=self.close)
        thread.daemon = True
        thread.start()
        
    def close(self):
        self.stop_thread_1_event.wait()         
        self.stop_thread_2_event.wait()         
        
        del self.root.city_popups[self.city]

        self.destroy()
        
        
    """-----------------------| Showing More Details |-----------------------
        Handles the request response and generating new popup with more data 
        to show like 5 days comparison and graph
    """
    def show_more_details(self):        
        try:
            self.get_forecast()
            ForecastPopup(self)
            
        except requests.exceptions.ConnectionError: 
            messagebox.showerror(title="Connection Error!!", message="Can't show more Details\nPlease Connect to the Internet!!")
            return
        except requests.Timeout: 
            messagebox.showerror(title="response time out!!", message="Can't show more Details\nTry again Later!!!")
            return
        except KeyError:
            messagebox.showerror(title="Not Found", message="Can't show more Details\nCity name is not present!!")
            return
        
        
    """-----------------------| Showing Traveling distance and route |-----------------------
        calculates the traveling distance and generate a downloadable HTML route map from your
        destination to the provided city
    """
    def show_traveling_distance_and_route(self):
        
        DirectionRoutes(self._lon, self._lat, self._city).get_distance_and_route()
        