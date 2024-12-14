import tkinter as tk
from PIL import Image, ImageTk
import utils.Macros as Macros


class CitiesFrame(tk.Frame):
    
    """---------------------| Cities Frame |---------------------
    Display Cities Frame, in which user can change:
        1. Add City.
        2. Remove City.
        3. Retrieve All Cities name.
    """
    def __init__(self, parent):
        super().__init__(parent, bg=Macros.APP_BG)
        
        self.cities = []
        
        self.remove_icon = ImageTk.PhotoImage(
            Image.open("./assets/close3.png").resize((14, 16))
        )
        
        self.column_count = 0
        self.row_count = 0
        self.max_columns = 4
        
        for col in range(self.max_columns):
            self.grid_columnconfigure(col, weight=1)


    """--------------------| Add City Label |--------------------
        Check first if the selected city exist or not if not make
        a new city Label and display it on the city list frame."""
    def add_label(self, label_text):
        
        for label_frame in self.cities:
            existing_label = label_frame.winfo_children()[0]  
            if existing_label.cget("text") == label_text:
                print(f"City '{label_text}' already exists.")
                return  
        
        label_frame = tk.Frame(self, bg=Macros.CYAN, bd=3, relief="sunken")
        
        new_label = tk.Label(label_frame, text=label_text, font=Macros.LABEL_FONT, fg=Macros.LABEL_FG, bg=Macros.CYAN)
        delete_button = tk.Button(label_frame, image=self.remove_icon, command=lambda: self.remove_label(label_frame), borderwidth=0, bg=Macros.CYAN)
        
        delete_button.bind("<Enter>", lambda e: on_enter(e))
        delete_button.bind("<Leave>", lambda e: on_exit(e))

        new_label.pack(side=tk.LEFT, padx=5, expand=True, fill="both")
        delete_button.pack(side=tk.RIGHT, padx=5)
        
        label_frame.grid(row=self.row_count, column=self.column_count, padx=5, pady=5, sticky="nsew")

        self.cities.append(label_frame)

        self.column_count += 1
        if self.column_count >= self.max_columns:
            self.column_count = 0
            self.row_count += 1
            
            
        """--------------------| Hovering the Close Button |--------------------
            just Change the styling of the frame on hover and revert on exit"""
        def on_enter(event):
            label_frame.configure(bg=Macros.LIGHT_RED)
            new_label.configure(bg=Macros.LIGHT_RED, fg="white")
            delete_button.configure(bg=Macros.LIGHT_RED)
            
        def on_exit(event):
            label_frame.configure(bg=Macros.CYAN)
            new_label.configure(bg=Macros.CYAN, fg=Macros.LABEL_FG)
            delete_button.configure(bg=Macros.CYAN)


    """--------------------| Remove City Label |--------------------
        remove the city label on clicking its corresponding delete button."""
    def remove_label(self, label_to_remove):
        label_to_remove.destroy()  
        
        self.cities.remove(label_to_remove)

        self.refresh_labels()


    """--------------------| Refresh Labels |--------------------
        Just Rerender the Label to maintain their order."""
    def refresh_labels(self):
        for widget in self.winfo_children():
            widget.grid_forget()

        self.column_count = 0
        self.row_count = 0

        for label in self.cities:
            
            label.grid(row=self.row_count, column=self.column_count, padx=5, pady=5, sticky="nsew")
            self.column_count += 1
            if self.column_count >= self.max_columns:
                self.column_count = 0
                self.row_count += 1
                
                
    """--------------------| Get all Cities |--------------------
        Return all Cities Names."""
    def get_cities(self):
        cities = []
        for label_frame in self.cities:
            existing_label = label_frame.winfo_children()[0]
            existing_city = existing_label.cget("text")
            cities.append(existing_city)

        return cities
