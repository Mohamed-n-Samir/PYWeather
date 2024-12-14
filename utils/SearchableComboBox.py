import tkinter as tk
from PIL import Image, ImageTk
import random


class SearchableComboBox(tk.Toplevel):
    
    """--------------------------------------| Searchable DropDown |--------------------------------------
    Display Dropdown popup, in which user can choose:
        1. Country Name
        2. City Name.
    and the chosen city is appended to the CitiesLabel
    """
    def __init__(self, parent, text, options, on_close, after_select = None) -> None:
        super().__init__(parent)
        self.dropdown_id = None
        self.options = options
        self.after_select = after_select
        self.text = text or "Select"

        self.title("Choose Country")
        self.geometry(f"200x200+{int(500 * random.random())}+50")
        self.resizable(False, False)
        self.attributes("-toolwindow", True)
        self.protocol("WM_DELETE_WINDOW", lambda: on_close())
        self.transient(parent)

        # ------------------------| Create a Text widget for the entry field |------------------------
        wrapper = tk.Frame(self)
        wrapper.pack(pady=10)

        self.entry = tk.Entry(wrapper, width=29)
        self.entry.insert(0, self.text)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", lambda event: self.on_focus_in(event, self.entry))
        self.entry.bind("<FocusOut>", lambda event: self.on_focus_out(event, self.entry))
        self.entry.pack(side=tk.LEFT)
        self.entry.lift()

        # ------------------------| Dropdown icon/button |------------------------
        self.icon = ImageTk.PhotoImage(
            Image.open("./assets/dropdown_arrow.png").resize((16, 16))
        )
        self.btn = tk.Button(wrapper, image=self.icon, command=self.show_dropdown)
        self.btn.pack(side=tk.LEFT)
        self.btn.lift()

        # ------------------------| Listbox widget for the dropdown menu |------------------------
        self.listbox = tk.Listbox(self, height=10)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        self.listbox.bind("<FocusOut>", self.hide_dropdown_on_focus_out) 
        for option in self.options:
            self.listbox.insert(tk.END, option)
            

    """--------------------------------------| Filtered Options |--------------------------------------
    Allow you to filter (search) the dropdown List on key entry:
    """
    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        if not typed_value:
            # If the entry is empty, display all options
            self.listbox.delete(0, tk.END)
            for option in self.options:
                self.listbox.insert(tk.END, option)
        else:
            # Filter options based on the typed value
            self.listbox.delete(0, tk.END)
            filtered_options = [
                option
                for option in self.options
                if option.lower().startswith(typed_value)
            ]

            for option in filtered_options:
                self.listbox.insert(tk.END, option)
        self.show_dropdown()



    """--------------------------------------| Selecting City |--------------------------------------
    Allow you to to Append the selected city to the thread list and the Cities Frame for UI:
    """
    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)
            
            if self.after_select != None:
                self.after_select(selected_option)


    """--------------------------------------| Show Dropdown List |--------------------------------------
    Allow you to visualize the List on dropdown button clicking or typing in entry box:
    """
    def show_dropdown(self, event=None):
        # Display the dropdown below the entry field
        self.listbox.place(in_=self.entry, x=-2, rely=1, relwidth=1.14, anchor="nw")


    """--------------------------------------| Hide Dropdown List |--------------------------------------
    Allow you to hide the List on Losing focus on the popup:
    """
    def hide_dropdown_on_focus_out(self, event=None):
        self.listbox.place_forget()
        
    def on_focus_in(self, event, entry):
        self.listbox.place(in_=self.entry, x=-2, rely=1, relwidth=1.14, anchor="nw")
        if entry.get() == self.text:
            entry.delete(0, tk.END)

    def on_focus_out(self, event, entry):
        if entry.get() == "":
            entry.insert(0, self.text)
            
        
    
    """--------------------------------------| Update the child (city) popup |--------------------------------------
    Allow you to Update the list options of the city list on selecting the country :
    """    
    def populate_listbox(self, options):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.text)
        self.listbox.delete(0, tk.END)
        for option in options:
            self.listbox.insert(tk.END, option)

    def update_options(self, new_options):
        self.options = new_options
        self.populate_listbox(new_options)
