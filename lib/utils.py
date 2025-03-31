import tkinter as tk

def create_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Kopiuj", command=lambda: widget.event_generate('<<Copy>>'))
    menu.add_command(label="Wklej", command=lambda: widget.event_generate('<<Paste>>'))
    menu.add_command(label="Wytnij", command=lambda: widget.event_generate('<<Cut>>'))
    widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))
