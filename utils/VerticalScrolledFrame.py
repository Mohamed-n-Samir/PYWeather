import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

class VerticalScrolledFrame(tk.Frame):
    
    """--------------------------------------| A Custom Made Frame that Allow Scrolling in TKinter |--------------------------------------
        A Tkinter scrollable frame that works and hides the scrollbar when no scrolling is needed
    """
    def __init__(self, parent, bg="red", *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        self.vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)

        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=self.vscrollbar.set, bg=bg)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = tk.Frame(self.canvas, bg=bg)
        interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

        # Update the scroll region of the canvas when the interior size changes
        def _configure_interior(event):
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            self._update_scrollbar_visibility()  # Update scrollbar visibility

        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                # Make sure the canvas adjusts to the inner frame width
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        def _on_mousewheel(event):
            """Handle the mouse wheel scroll event."""
            if self.canvas.bbox("all") is None:  # Check if there is no content to scroll
                return
            if self.canvas.winfo_height() < self.canvas.bbox("all")[3]:
                if event.num == 5 or event.delta == -120:  # Scroll down
                    self.canvas.yview_scroll(1, "units")
                elif event.num == 4 or event.delta == 120:  # Scroll up
                    self.canvas.yview_scroll(-1, "units")

        self.canvas.bind('<Configure>', _configure_canvas)
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)


    """--------------------------------------| Update Scrollbar Visibility |--------------------------------------
        Show A scrollbar on components overflow and hide it on components underflow
    """
    def _update_scrollbar_visibility(self):
        """Hide or show the scrollbar based on the content's size."""
        if self.canvas.bbox("all") is not None:
            content_height = self.canvas.bbox("all")[3]  # Bottom edge of the content
            canvas_height = self.canvas.winfo_height()

            if content_height > canvas_height:
                # Content exceeds the canvas height, show the scrollbar
                self.vscrollbar.pack(side=RIGHT, fill=Y, expand=FALSE)
            else:
                # Content fits within the canvas, hide the scrollbar
                self.vscrollbar.pack_forget()


