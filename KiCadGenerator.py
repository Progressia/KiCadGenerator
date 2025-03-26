import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

# Wczytaj template.json przy starcie
try:
    with open("template.json", "r", encoding="utf-8") as f:
        sample_json = f.read()
except FileNotFoundError:
    sample_json = "// template.json not found"

class KiCadSchGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("KiCad .kicad_sch Generator")
        self.geometry("600x450")

        # A. Ścieżka + przycisk PATH
        path_frame = tk.Frame(self)
        path_frame.pack(pady=(10, 0), padx=10, fill="x")

        tk.Label(path_frame, text="Ścieżka do symboli KiCad:").pack(side="left")
        self.path_entry = tk.Entry(path_frame, width=50)
        self.path_entry.pack(side="left", padx=5, expand=True, fill="x")
        self.path_entry.insert(0, "/usr/share/kicad/symbols")

        path_button = tk.Button(path_frame, text="PATH", command=self.choose_path)
        path_button.pack(side="left")

        # C. Duże pole tekstowe z przykładowym tekstem
        tk.Label(self, text="Treść pliku .kicad_sch:").pack(pady=(10, 0))
        self.text_area = tk.Text(self, wrap="word", height=15)
        self.text_area.pack(expand=True, fill="both", padx=10, pady=5)
        self.text_area.insert("1.0", sample_json)

        # B. Skróty Ctrl+C / Ctrl+V
        self.text_area.bind("<Control-c>", lambda e: self.copy_text())
        self.text_area.bind("<Control-v>", lambda e: self.paste_text())

        # D. Przycisk Generate
        generate_button = tk.Button(self, text="Generate .kicad_sch", command=self.generate_file)
        generate_button.pack(pady=10)

    def choose_path(self):
        selected_path = filedialog.askdirectory(initialdir=self.path_entry.get())
        if selected_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_path)

    def copy_text(self):
        try:
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.clipboard_clear()
            self.clipboard_append(selected_text)
        except tk.TclError:
            pass

    def paste_text(self):
        try:
            self.text_area.insert(tk.INSERT, self.clipboard_get())
        except tk.TclError:
            pass

    def generate_file(self):
        content = self.text_area.get("1.0", tk.END).strip()
        filename = "output.kicad_sch"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Sukces", f"Plik '{filename}' został zapisany.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")
            
if __name__ == "__main__":
    app = KiCadSchGenerator()
    app.mainloop()
