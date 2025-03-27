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
        self.geometry("1200x600")

        # A. Ścieżka + przycisk PATH
        path_frame = tk.Frame(self)
        path_frame.pack(pady=(10, 0), padx=10, fill="x")
        tk.Label(path_frame, text="Ścieżka do symboli KiCad:").pack(side="left")

        self.path_entry = tk.Entry(path_frame, width=50)
        self.path_entry.pack(side="left", padx=5, expand=True, fill="x")
        self.path_entry.insert(0, "/usr/share/kicad/symbols")

        path_button = tk.Button(path_frame, text="PATH", command=self.choose_path)
        path_button.pack(side="left")

        # Przycisk Add pod ścieżką
        add_button = tk.Button(self, text="Add", command=self.open_add_window)
        add_button.pack(pady=(5, 0))

        # C. Pole tekstowe JSON i wygenerowany kicad_sch obok siebie
        editor_frame = tk.Frame(self)
        editor_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # JSON input
        json_frame = tk.Frame(editor_frame)
        json_frame.pack(side="left", expand=True, fill="both", padx=(0, 5))
        tk.Label(json_frame, text="Wejściowy JSON:").pack()
        self.text_area = tk.Text(json_frame, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.text_area.insert("1.0", sample_json)

        # Środkowa strzałka (przycisk)
        arrow_frame = tk.Frame(editor_frame)
        arrow_frame.pack(side="left", padx=5)
        arrow_button = tk.Button(arrow_frame, text="→", font=("Arial", 14), command=self.transfer_text)
        arrow_button.pack(pady=20)

        # KiCad output
        sch_frame = tk.Frame(editor_frame)
        sch_frame.pack(side="left", expand=True, fill="both", padx=(5, 0))
        tk.Label(sch_frame, text="Wygenerowany plik KiCad:").pack()
        self.output_area = tk.Text(sch_frame, wrap="word", state="normal")
        self.output_area.pack(expand=True, fill="both")

        # Skróty Ctrl+C / Ctrl+V
        self.text_area.bind("<Control-c>", lambda e: self.copy_text())
        self.text_area.bind("<Control-v>", lambda e: self.paste_text())

        # Przycisk Save
        save_button = tk.Button(self, text="Save .kicad_sch", command=self.save_file)
        save_button.pack(pady=10)

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

    def transfer_text(self):
        content = self.text_area.get("1.0", tk.END).strip()
        self.output_area.config(state="normal")
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert("1.0", content)
        self.output_area.config(state="normal")

    def save_file(self):
        content = self.output_area.get("1.0", tk.END).strip()
        filename = "output.kicad_sch"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Sukces", f"Plik '{filename}' został zapisany.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się zapisać pliku: {e}")

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Dodaj komponent")
        add_window.geometry("300x200")
        # Opcje trybu dodawania
        self.add_mode = tk.StringVar(value="component")  # domyślnie component

        radio_frame = tk.Frame(add_window)
        radio_frame.pack(pady=(10, 5))

        tk.Radiobutton(radio_frame, text="Component", variable=self.add_mode, value="component", command=self.update_add_form).pack(side="left", padx=5)
        tk.Radiobutton(radio_frame, text="Connection", variable=self.add_mode, value="connection", command=self.update_add_form).pack(side="left", padx=5)
        tk.Radiobutton(radio_frame, text="Module", variable=self.add_mode, value="module", command=self.update_add_form).pack(side="left", padx=5)

        # Kontener na formularz (będzie się zmieniać dynamicznie)
        self.form_frame = tk.Frame(add_window)
        self.form_frame.pack(pady=10, fill="both", expand=True)

        # Wywołaj pierwszy raz, żeby zainicjować widok
        self.update_add_form()

    def update_add_form(self):
        # Wyczyść poprzednie elementy formularza
        for widget in self.form_frame.winfo_children():
            widget.destroy()

        mode = self.add_mode.get()

        if mode == "component":
            tk.Label(self.form_frame, text="Dodawanie komponentu (TODO)").pack()
        elif mode == "connection":
            tk.Label(self.form_frame, text="Dodawanie połączenia (TODO)").pack()
        elif mode == "module":
            tk.Label(self.form_frame, text="Dodawanie modułu (TODO)").pack()

if __name__ == "__main__":
    app = KiCadSchGenerator()
    app.mainloop()
