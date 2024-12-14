from tkinter import Frame, Label, LabelFrame, Toplevel
from PIL import Image, ImageTk

from matplotlib.figure import Figure
from matplotlib.widgets import Cursor
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Classes.Root import RootSingleton

class ForecastPopup(Toplevel):
    
    """---------------------| Five Days Data Forecasting |---------------------
    Display A popup, in which user can Can See:
        1. The Data of the next 5 days for the same city.
        2. Graph representing the 5 Days Temp.
    """
    def __init__(self,parent):
        super().__init__(parent)
        self.master = parent
        self.root = RootSingleton()
        self.title(f"{self.master.city} In Next 5 Days")
        self.wm_iconbitmap(self.root.ICON)

        self.resizable(False,False)
        
        self.forecast_details = self.master.forecast_details()
        
        self.FF_Frame()
        self.FF_graph()
    
    
    """--------------------------| Five Weather Forecast Frame |--------------------------
    Make five Forecast Frame which includes:
    -> A main frame which includes 5 frames
    -> Each Subframe will display the Date, Temperature, Day, night temp"""
    def FF_Frame(self) -> None:

        #----------| Five Weather Forecast Frame |----------
        self.FF_details = self.forecast_details
        self.five_Forecast = Frame(self, bg=self.FF_details[0]["bg color"], pady=27)
        self.images = []
        
        for idx, day in enumerate(self.FF_details):
            if not idx:
                day['Date'] = "Tomorrow"
            
            #============================| Day Frame |============================
            day_frame = Frame(self.five_Forecast, bg=day["bg color"])
            #----------| day_frame Date |----------
            TDate = Label(day_frame, text=day["Date"], font=("Tahoma", 18), justify="center", bg=day["bg color"])
            TDate.pack(side="top", fill="x")

            #----------| day_frame Weather |----------
            TWeather = LabelFrame(day_frame, text=f'{int(day["Temp"]):>3}°{self.root.default_unit.lower()}\n{day["Name"]}',
            font=("Tahoma", 18), labelanchor="s", relief="flat", bg=day["bg color"])
            Timg = ImageTk.PhotoImage(Image.open(day["Image"]).resize(day["Image size"]))
            self.images.append(Timg)
            TW_image = Label(TWeather, image=Timg, bg=day["bg color"])
            TW_image.pack(side="top", fill="both", pady=day["Image pady"])
            TWeather.pack(side="top", fill="x", pady=20)

            #----------| day_frame Day Temp|----------
            TDay = Label(day_frame, text=f" {'Day:':<9}{int(day['Day:']):>3}°{self.root.default_unit.lower()}",
            font=("Tahoma", 14), justify="center", bg=day["bg color"])
            TDay.pack(side="top", fill="x")

            #----------| day_frame Night Temp |----------
            TNight = Label(day_frame, text=f" {'Night:':<9}{int(day['Night:']):>3}°{self.root.default_unit.lower()}",
            font=("Tahoma", 14), justify="center", bg=day["bg color"])
            TNight.pack(side="top", fill="x")
            day_frame.grid(row=0, column=idx, sticky="nswe", ipadx=day["Frame ipadx"], ipady=5)

        #----------| Extra pad space to cover empty area |----------
        self.extra = Frame(self.five_Forecast)
        self.extra.grid(row=0, column=7, padx=5)
        self.five_Forecast.pack(fill="both", expand=1)
        
        self.update()

    
    """--------------------------| five Weather Forecast Graph |--------------------------
    Display the graph of the 5 days temperature"""
    def FF_graph(self) -> None:
        
        #----------| 5 Weather Forecast Frame |----------
        self.F_WForecast = Frame(self, bg="cyan")
        self.F_WForecast.pack(anchor="nw", side="top", fill="both", expand=1)

        #---------------------| Figure area for Graph |---------------------
        self.five_fig = Figure(figsize=(7.3, 3.5), dpi=100, facecolor=self.FF_details[0]["light color"], tight_layout={'h_pad' : 3})

        #---------------------| Data which display in Graph |---------------------
        details = self.forecast_details
        self.Dates = [ day["Date"] for day in details]
        self.Temps = [ day["Temp"] for day in details]

        #---------------------| Plotting Line Graph |---------------------
        self.five_graph = self.five_fig.add_subplot(111)
        self.five_graph.plot(self.Dates, self.Temps, color="black", linestyle="-", linewidth=3, marker="o", markersize=9, markerfacecolor=self.FF_details[0]["bg color"])
        self.five_graph.set_title(label="Temperature of next 5 days", fontdict={"fontfamily" : "Tahoma", "fontsize": 16}, color="black")
        self.five_graph.set_facecolor(self.FF_details[0]["light color"])
        self.five_graph.spines["right"].set_visible(False)
        self.five_graph.spines["top"].set_visible(False)
        self.five_graph.spines["left"].set_visible(False)
        self.five_graph.spines["bottom"].set_color("black")

        #---------------------| Labels and ticks on X-axis |---------------------
        self.X_ticks = [date for date in self.Dates]
        self.five_graph.set_xticks(self.Dates)
        self.five_graph.set_xticklabels(labels=self.X_ticks, fontfamily="Tahoma", fontsize=12, color="black")
        self.five_graph.set_xlabel(xlabel="Date", color="black", fontfamily="Tahoma", fontsize=14)

        #---------------------| Labels and ticks on Y-axis |---------------------
        self.five_graph.set_yticks([])

        #---------------------| Cursor which spanes the axis when mouse moves over |---------------------
        Cursor(ax=self.five_graph, horizOn=False, vertOn=False, useblit=True,
                        color = "r", linewidth = 1)

        #---------------------| Annotated box on which clicked area temp. display |---------------------
        self.five_annot = self.five_graph.annotate(text="", xy=(self.X_ticks[0], 0), xytext=(10, 20),
            textcoords="offset points", arrowprops={"arrowstyle" : "fancy"}, annotation_clip=True,
            bbox={"boxstyle" : "round, pad=0.5", "fc" : self.FF_details[0]["light color"], "ec" : "black", "lw" : 2}, size=10)
        self.five_annot.set_visible(True)

        #---------------------| Canvas to place the Graph Figure |---------------------
        self.five_canvas = FigureCanvasTkAgg(figure=self.five_fig, master=self.F_WForecast)
        self.five_canvas.mpl_connect('button_press_event', self.FF_show_temp)
        self.five_canvas.draw()
        self.five_canvas.get_tk_widget().grid(row=2, column=0, sticky="nw")
        
        
    """---------------------| Shows the 5 selected point temp in graph |---------------------
    It will call upon when mouse button is clicked on temperature line graph"""
    def FF_show_temp(self, event) -> None:

        Wcoord = []
        Wcoord.append((event.xdata, event.ydata))
        Wx = event.xdata
        Wy = event.ydata
        
        # Setting the temperature based on axis
        self.five_annot.xy = (Wx, Wy)
        try:
            self.five_annot.set_text(f"{self.Temps[int(Wx)]}°{self.root.default_unit.lower()}")
            self.five_annot.set_visible(True)
            self.five_canvas.draw()
        except TypeError:   # if mouse axis is out of ploted area
            pass

