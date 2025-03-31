import tkinter as tk

def create_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Kopiuj", command=lambda: widget.event_generate('<<Copy>>'))
    menu.add_command(label="Wklej", command=lambda: widget.event_generate('<<Paste>>'))
    menu.add_command(label="Wytnij", command=lambda: widget.event_generate('<<Cut>>'))
    widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

def enable_shortcuts(widget):
    # CTRL+C
    widget.bind("<Control-c>", lambda e: widget.event_generate("<<Copy>>"))
    # CTRL+V
    widget.bind("<Control-v>", lambda e: widget.event_generate("<<Paste>>"))
    # CTRL+A – zaznacz wszystko
    widget.bind("<Control-a>", lambda e: select_all(e, widget))
    widget.bind("<Control-A>", lambda e: select_all(e, widget))  # dla dużych liter

def select_all(event, widget):
    widget.tag_add("sel", "1.0", "end-1c")
    return "break"  # zatrzymaj propagację zdarzenia (żeby nie pisnęło „a”)
