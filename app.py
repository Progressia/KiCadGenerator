import tkinter as tk
from tkinter import filedialog
import os
import json
from lib.parser import parse_kicad_sym, parse_kicad_sch

class KiCadSymbolImporter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("KiCad Symbol Importer")
        self.geometry("1000x600")

        # Przycisk Import
        import_button = tk.Button(self, text="Import", command=self.import_file)
        import_button.pack(pady=10)

        # Ramka dla dwóch pól tekstowych obok siebie
        text_frame = tk.Frame(self)
        text_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Scrollbar i pole tekstowe dla RAW
        self.text_area_raw = tk.Text(text_frame, wrap="none")
        scroll_raw_y = tk.Scrollbar(text_frame, orient="vertical", command=self.text_area_raw.yview)
        scroll_raw_x = tk.Scrollbar(text_frame, orient="horizontal", command=self.text_area_raw.xview)
        self.text_area_raw.configure(yscrollcommand=scroll_raw_y.set, xscrollcommand=scroll_raw_x.set)

        self.text_area_raw.grid(row=0, column=0, sticky="nsew")
        scroll_raw_y.grid(row=0, column=1, sticky="ns")
        scroll_raw_x.grid(row=1, column=0, sticky="ew")

        # Scrollbar i pole tekstowe dla JSON
        self.text_area_json = tk.Text(text_frame, wrap="none")
        scroll_json_y = tk.Scrollbar(text_frame, orient="vertical", command=self.text_area_json.yview)
        scroll_json_x = tk.Scrollbar(text_frame, orient="horizontal", command=self.text_area_json.xview)
        self.text_area_json.configure(yscrollcommand=scroll_json_y.set, xscrollcommand=scroll_json_x.set)

        self.text_area_json.grid(row=0, column=2, sticky="nsew")
        scroll_json_y.grid(row=0, column=3, sticky="ns")
        scroll_json_x.grid(row=1, column=2, sticky="ew")

        # Konfiguracja rozciągania kolumn
        text_frame.grid_columnconfigure(0, weight=1)
        text_frame.grid_columnconfigure(2, weight=1)
        text_frame.grid_rowconfigure(0, weight=1)

        # Obsługa menu kontekstowego
        self._create_context_menu(self.text_area_raw)
        self._create_context_menu(self.text_area_json)

    def _create_context_menu(self, widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Kopiuj", command=lambda: widget.event_generate('<<Copy>>'))
        menu.add_command(label="Wklej", command=lambda: widget.event_generate('<<Paste>>'))
        menu.add_command(label="Wytnij", command=lambda: widget.event_generate('<<Cut>>'))
        widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

    def import_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="/usr/share/kicad/symbols/",
            filetypes=[("KiCad Files", "*.kicad_sym *.kicad_sch"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_area_raw.delete("1.0", tk.END)
                self.text_area_raw.insert("1.0", content)

                ext = os.path.splitext(file_path)[1]
                parsed = {}

                if ext == ".kicad_sym":
                    parsed = parse_kicad_sym(content)
                elif ext == ".kicad_sch":
                    parsed = parse_kicad_sch(content)
                else:
                    parsed = {"error": "Nieobsługiwane rozszerzenie."}

                self.text_area_json.delete("1.0", tk.END)
                self.text_area_json.insert("1.0", json.dumps(parsed, indent=2))

            except Exception as e:
                self.text_area_raw.delete("1.0", tk.END)
                self.text_area_raw.insert("1.0", f"Błąd podczas importu pliku:\n{e}")

if __name__ == "__main__":
    app = KiCadSymbolImporter()
    app.mainloop()
