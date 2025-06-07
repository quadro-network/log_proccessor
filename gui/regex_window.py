import tkinter as tk
from tkinter import filedialog, messagebox
import re
import os
import json


class RegexSearchWindow:
    def __init__(self, parent, file_path):
        self.file_path = file_path
        self.window = tk.Toplevel(parent)
        self.window.title("Поиск по регулярному выражению")
        self.window.geometry("700x500")

        tk.Label(self.window, text="Введи рег.выражение", font=("Arial", 10)).pack(pady=5)

        self.entry = tk.Entry(self.window, font=("Courier", 12), width=60)
        self.entry.pack(pady=5)
        self.entry.focus_set()

        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="Сохранить результат", bg="#6A5ACD", fg="white", command=self.save_result).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Шаблоны", bg="#6A5ACD", fg="white", command=self.show_templates).pack(side=tk.LEFT, padx=5)

        self.output = tk.Text(self.window, wrap=tk.WORD)
        self.output.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.templates_path = "config/regex_templates.json"
        self.templates = self.load_templates()

    def load_templates(self):
        if os.path.exists(self.templates_path):
            try:
                with open(self.templates_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                messagebox.showwarning("Ошибка загрузки шаблонов", str(e))
        return []

    def show_templates(self):
        template_window = tk.Toplevel(self.window)
        template_window.title("Шаблоны регулярных выражений")
        template_window.geometry("500x300")
        tk.Label(template_window, text="Выберите шаблон:", font=("Arial", 10)).pack(pady=5)

        for tpl in self.templates:
            desc = tpl.get("description", "Без описания")
            pattern = tpl.get("pattern", "")
            button = tk.Button(template_window, text=f"{desc}", anchor="w", justify="left",
                               command=lambda p=pattern: self.entry.delete(0, tk.END) or self.entry.insert(0, p))
            button.pack(fill=tk.X, padx=10, pady=2)

    def save_result(self):
        pattern = self.entry.get().strip()
        if not pattern:
            messagebox.showwarning("Ошибка", "Введите регулярное выражение.")
            return

        try:
            regex = re.compile(pattern)
        except re.error as e:
            messagebox.showerror("Ошибка", f"Некорректное регулярное выражение:\n{e}")
            return

        matches = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                found = regex.findall(line)
                if found:
                    if isinstance(found, list):
                        matches.extend(found)
                    else:
                        matches.append(found)

        if not matches:
            messagebox.showinfo("Результат", "Совпадений не найдено.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="regex_results.txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )

        if save_path:
            with open(save_path, "w", encoding="utf-8") as out:
                for m in matches:
                    out.write(m + "\n")
            self.output.delete("1.0", tk.END)
            self.output.insert(tk.END, f"Сохранено: {save_path}\n\n")
            self.output.insert(tk.END, "\n".join(matches))
