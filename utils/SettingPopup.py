from tkinter import messagebox, Label, Button, StringVar, Entry, Toplevel, Frame, LabelFrame, Radiobutton
from Classes.Root import RootSingleton 

import utils.Macros as Macros



class SettingPopup(Toplevel):
    
    """--------------------------------------| Settings Window |--------------------------------------
    Display Settings window, in which user can change:
        1. Api Token
        2. Default City.
        3. Units in which temperature is shown.
    """
    def __init__(self, parent=None):
        super().__init__(parent, bg=Macros.GRAY)

        self.root = RootSingleton()

        # --------------------------------------| Settings Window |--------------------------------------
        self.focus()
        self.title("Weather App - Settings")
        self.geometry("420x420")
        self.resizable(False, False)
        self.transient(parent)
        self.wm_iconbitmap(self.root.ICON)

        # --------------------------------------| Settings Label |--------------------------------------
        self.setting_label = Label(
            self,
            text="Settings",
            font=Macros.HEADER_FONT,
            bg=Macros.GRAY,
            fg=Macros.GOLD,
            justify="center",
        )
        self.setting_label.pack(side="top", fill="x", pady=5)
        self.set_sep1 = Frame(self, bg="black")
        self.set_sep1.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # --------------------------| New API Token Label |--------------------------
        self.new_api_label = LabelFrame(
            self,
            text="• Update API Token to Start Running the app",
            font=("Arial", 14),
            bg=Macros.GRAY,
            labelanchor="nw",
            relief="flat",
        )
        
        # ----------| New API Token Entry |----------
        self.new_api = StringVar()
        self.new_api_entry = Entry(
            self.new_api_label,
            text=self.new_api,
            font=("Arial", 12),  
            # bg=Macros.CYAN,
            relief="solid",
            highlightthickness=1,
            highlightbackground="black",
            justify="center",
            width=41
        )
        self.new_api_entry.grid(
            row=0, column=0, sticky="nswe", ipady=5, padx=10, pady=10
        )
        
        self.new_api.set(self.root.default_api_token if self.root.default_api_token != None else "")
        
        self.new_api_entry.bind(
            "<KeyRelease>", lambda e: self.new_api.set(self.new_api_entry.get())
        )



        self.new_api_label.pack(side="top", anchor="nw", ipadx=10, padx=10, pady=5)
        self.set_sep2 = Frame(self, bg="black")
        self.set_sep2.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # --------------------------| New Location Label |--------------------------
        self.new_loc_label = LabelFrame(
            self,
            text="• Update City name to show weather at start",
            font=("Arial", 14),
            bg=Macros.GRAY,
            labelanchor="nw",
            relief="flat",
        )
        
        # ----------| New Location Entry |----------
        self.new_loc = StringVar()
        self.new_loc_entry = Entry(
            self.new_loc_label,
            text=self.new_loc,
            font=("Arial", 12),  
            # bg=Macros.CYAN,
            relief="solid",
            highlightthickness=1,
            highlightbackground="black",
            justify="center",
            width=41
        )
        self.new_loc_entry.grid(
            row=0, column=0, sticky="nswe", ipady=5, padx=10, pady=10
        )
        self.new_loc.set(self.root.default_city if self.root.default_city != None else "")
        
        self.new_loc_entry.bind(
            "<KeyRelease>", lambda e: self.new_loc.set(self.new_loc_entry.get())
        )

        self.new_loc_label.pack(side="top", anchor="nw", ipadx=10, padx=10, pady=5)
        self.set_sep2 = Frame(self, bg="black")
        self.set_sep2.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # --------------------------| Temperature Unit Label |--------------------------
        self.Temp_label = LabelFrame(
            self,
            text="• Temperature Unit",
            font=("Arial", 14),
            bg=Macros.GRAY,
            labelanchor="nw",
            relief="flat",
        )
        # ----------| Celsius |----------
        self.unit_var = StringVar()
        self.unit_var.set(self.root.default_unit)
        self.Celsius_radio = Radiobutton(
            self.Temp_label,
            font=("Arial", 14),
            text=self.root.UNITS["C"][0],
            variable=self.unit_var,
            value="C",
            bg=Macros.GRAY,
            activebackground=Macros.GOLD,
            # selectcolor=Macros.GRAY,
            relief="flat",
            overrelief="solid",
        )
        self.Celsius_radio.grid(row=0, column=0, sticky="ne", ipadx=5)

        # ----------| Farheniet |----------
        self.Fahreneit_radio = Radiobutton(
            self.Temp_label,
            font=("Arial", 14),
            text=self.root.UNITS["F"][0],
            variable=self.unit_var,
            value="F",
            bg=Macros.GRAY,
            activebackground=Macros.GOLD,
            # selectcolor=Macros.GRAY,
            relief="flat",
            overrelief="solid",
        )
        self.Fahreneit_radio.grid(row=0, column=1, sticky="nswe")

        self.Temp_label.pack(side="top", anchor="nw", ipadx=10, padx=10, pady=5)
        self.set_sep3 = Frame(self, bg="black")
        self.set_sep3.pack(side="top", anchor="nw", fill="x", padx=10, pady=5)

        # --------------------------| Bottom Buttons |--------------------------
        self.buttons_frame = Frame(self, bg=Macros.GRAY)

        self.bottom_sep1 = Frame(self.buttons_frame, bg=Macros.GRAY)
        self.bottom_sep1.grid(row=0, column=0, padx=60)

        # ----------| Apply Button |----------
        self.apply_button = Button(
            self.buttons_frame,
            text="Apply",
            font=("Arial", 12),
            bg=Macros.GRAY,
            relief="solid",
            overrelief="solid",
            activebackground=Macros.GOLD,
            command=self.apply_settings
        )
        self.apply_button.grid(row=0, column=1, ipadx=10, padx=10, pady=5)

        # ----------| Reset Button |----------
        self.reset_button = Button(
            self.buttons_frame,
            text="Reset",
            font=("Arial", 12),
            bg=Macros.GRAY,
            relief="solid",
            overrelief="solid",
            activebackground=Macros.GOLD,
            command=self.reset_settings
        )
        self.reset_button.grid(row=0, column=2, ipadx=10, padx=10, pady=5)

        self.buttons_frame.pack(side="top", fill="x", pady=5)

        # --------------------| Bindings |--------------------
        
        self.Celsius_radio.bind(
            "<Enter>", lambda e: self.Celsius_radio.configure(bg=Macros.GOLD)
        )
        self.Celsius_radio.bind(
            "<Leave>", lambda e: self.Celsius_radio.configure(bg=Macros.GRAY)
        )

        self.Fahreneit_radio.bind(
            "<Enter>", lambda e: self.Fahreneit_radio.configure(bg=Macros.GOLD)
        )
        self.Fahreneit_radio.bind(
            "<Leave>", lambda e: self.Fahreneit_radio.configure(bg=Macros.GRAY)
        )

        self.apply_button.bind(
            "<Enter>", lambda e: self.apply_button.configure(bg=Macros.GOLD)
        )
        self.apply_button.bind(
            "<Leave>", lambda e: self.apply_button.configure(bg=Macros.GRAY)
        )

        self.reset_button.bind(
            "<Enter>", lambda e: self.reset_button.configure(bg=Macros.GOLD)
        )
        self.reset_button.bind(
            "<Leave>", lambda e: self.reset_button.configure(bg=Macros.GRAY)
        )


    """--------------------| Reset Settings |--------------------
        Reset All Setting to it's Defualt Value."""
    def reset_settings(self) -> None:

        try:
            if messagebox.askyesno("Warning", "Are you sure you want\nto restore the defults and delete the\nAPI Token!!!"):

                with open("./assets/location.txt", "w+") as file:
                    self.new_loc.set("Cairo")
                    file.write(self.new_loc_entry.get().capitalize())
                    file.seek(0)
                    self.root.default_city = file.read()

                with open("./assets/unit.txt", "w+") as file:
                    self.unit_var.set("C")
                    file.write(self.unit_var.get())
                    file.seek(0)
                    self.root.default_unit = file.read()
                
                with open("./assets/api_token.txt", "w+") as file:
                    self.new_api.set("")
                    file.write(self.new_api.get())
                    file.seek(0)
                    self.root.default_api_token = file.read()
                    
                messagebox.showinfo("Successful", "Update done Successfully!")
                
        except Exception as e:
            print(e)
    
    
    """--------------------| Apply Settings |--------------------
        Update all Changed Values."""   
    def apply_settings(self) -> None:
        try:
            if (self.new_loc_entry.get().strip() not in ["", None] and self.new_loc_entry.get().strip().capitalize() not in self.root.get_all_cities()) :
                messagebox.showwarning("Weather App", message="We Don't have Data on the\nProvided City Please Change it!")
                return

            if len(self.new_api.get().strip()) != 32 :
                messagebox.showwarning("Weather App", message="Please Enter a Correct Token")
                return

            with open("./assets/location.txt", "w+") as loc:
                if self.new_loc_entry.get().strip() not in ["", None]:
                    loc.write(self.new_loc_entry.get().strip().capitalize())
                    loc.seek(0)
                    self.root.default_city = loc.read()

            with open("./assets/unit.txt", "w+") as u:
                u.write(self.unit_var.get().strip())
                u.seek(0)
                self.root.default_unit = u.read()

            with open("./assets/api_token.txt", "w+") as v:
                v.write(self.new_api.get().strip())
                v.seek(0)
                self.root.default_api_token = v.read()
                 
            if self.root.default_city not in ["", None] : self.master.cities_frame.add_label(self.root.default_city)
            
            messagebox.showinfo("Successful", "Update done Successfully!")
            
        
        except Exception as e:
            print(e)
        
