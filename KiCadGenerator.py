import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json
import uuid
from datetime import datetime

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
        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            messagebox.showerror("Błąd JSON", f"Nieprawidłowy JSON: {e}")
            return

        lib_section = self.generate_lib_symbols(data.get("lib_symbols", [])) if "lib_symbols" in data else ""

        final_output = f"""(kicad_sch
  (version {data.get("version", "20250114")})
  (generator \"{data.get("generator", "eeschema")}\")
  (generator_version \"{data.get("generator_version", "9.0")}\")
  (uuid \"{str(uuid.uuid4())}\")
  (paper \"{data.get("paper", "A3")}\")

  {lib_section}
)
"""

        self.output_area.config(state="normal")
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert("1.0", final_output)
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

    def generate_lib_symbols(self, lib_symbols):
        result = ["(lib_symbols"]
        for sym in lib_symbols:
            result.append(f'  (symbol "{sym["name"]}")')
            result.append('    (pin_numbers (hide yes))')
            result.append('    (pin_names (offset 0))')
            result.append('    (exclude_from_sim no)')
            result.append('    (in_bom yes)')
            result.append('    (on_board yes)')
            result.append(f'    (property "Reference" "{sym["reference"]}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append(f'    (property "Value" "{sym["value"]}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append(f'    (property "Footprint" "" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append(f'    (property "Datasheet" "~" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append(f'    (property "Description" "{sym["description"]}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append(f'    (property "ki_keywords" "{sym["keywords"]}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append(f'    (property "ki_fp_filters" "{sym["fp_filters"]}" (at 0 0 0) (effects (font (size 1.27 1.27)) (hide yes)))')
            result.append('    (embedded_fonts no)')
            result.append('  )')
        result.append(')')
        return "\n".join(result)

    def open_add_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Dodaj komponent")
        add_window.geometry("300x250")

        tk.Label(add_window, text="Wybierz typ elementu:").pack(pady=(10, 5))
        selected_type = tk.StringVar(value="symbol")

        radio_frame = tk.Frame(add_window)
        radio_frame.pack(pady=5)

        content_frame = tk.Frame(add_window)
        content_frame.pack(pady=10)

        def update_content():
            for widget in content_frame.winfo_children():
                widget.destroy()
            if selected_type.get() == "symbol":
                tk.Label(content_frame, text="Dodajesz SYMBOL").pack()
            elif selected_type.get() == "module":
                tk.Label(content_frame, text="Dodajesz MODULE").pack()

        tk.Radiobutton(radio_frame, text="Symbol", variable=selected_type, value="symbol", command=update_content).pack(side="left", padx=10)
        tk.Radiobutton(radio_frame, text="Module", variable=selected_type, value="module", command=update_content).pack(side="left", padx=10)

        update_content()

        def confirm_add():
            try:
                content = self.text_area.get("1.0", tk.END).strip()
                data = json.loads(content)
                if "lib_symbols" not in data:
                    data["lib_symbols"] = []
                if "symbols" not in data:
                    data["symbols"] = []
                updated = json.dumps(data, indent=2)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", updated)
                add_window.destroy()
            except json.JSONDecodeError:
                messagebox.showerror("Błąd", "Nieprawidłowy JSON")

        button_frame = tk.Frame(add_window)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="OK", command=confirm_add).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", command=add_window.destroy).pack(side="left")

if __name__ == "__main__":
    app = KiCadSchGenerator()
    app.mainloop()
