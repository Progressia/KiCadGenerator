import tkinter as tk
from tkinter import filedialog

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

        # Pole tekstowe do wyświetlania zawartości pliku .kicad_sym
        self.text_area_raw = tk.Text(text_frame, wrap="word")
        self.text_area_raw.pack(side="left", expand=True, fill="both", padx=(0, 5))

        # Pole tekstowe do wyświetlania JSON po konwersji
        self.text_area_json = tk.Text(text_frame, wrap="word")
        self.text_area_json.pack(side="left", expand=True, fill="both", padx=(5, 0))

    def import_file(self):
        file_path = filedialog.askopenfilename(
            initialdir="/usr/share/kicad/symbols/",
            filetypes=[("KiCad Symbol Files", "*.kicad_sym"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_area_raw.delete("1.0", tk.END)
                self.text_area_raw.insert("1.0", content)

                # Tu w przyszłości będzie parser do JSON:
                self.text_area_json.delete("1.0", tk.END)
                self.text_area_json.insert("1.0", "// Tu będzie wynik parsowania na JSON")

            except Exception as e:
                self.text_area_raw.delete("1.0", tk.END)
                self.text_area_raw.insert("1.0", f"Błąd podczas importu pliku:\n{e}")

if __name__ == "__main__":
    app = KiCadSymbolImporter()
    app.mainloop()
