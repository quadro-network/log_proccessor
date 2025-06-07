import tkinter as tk
from tkinter import filedialog, messagebox
import os

class DuplicatesWindow:
    def __init__(self, parent, file_path=None):
        self.file_path = file_path

        self.window = tk.Toplevel(parent)
        self.window.title("Поиск дублей")
        self.window.geometry("400x250")

        tk.Button(self.window, text="Добавить файл", command=self.select_file, fg="blue").pack(pady=5)
        self.file_label = tk.Label(
            self.window,
            text=os.path.basename(file_path) if file_path else "Файл не выбран",
            fg="black" if file_path else "gray"
        )
        self.file_label.pack()

        tk.Label(self.window, text="Игнорировать начало:").pack()
        self.ignore_start_entry = tk.Entry(self.window)
        self.ignore_start_entry.pack(pady=2)

        tk.Label(self.window, text="Игнорировать середину (напр. \\u001d93):").pack()
        self.ignore_middle_entry = tk.Entry(self.window)
        self.ignore_middle_entry.pack(pady=2)

        tk.Button(self.window, text="Искать дубли", command=self.find_duplicates).pack(pady=10)

    def select_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if path:
            self.file_path = path
            self.file_label.config(text=os.path.basename(path), fg="black")

    def clean_code(self, code, ignore_start, ignore_middle):
        if ignore_start and code.startswith(ignore_start):
            code = code[len(ignore_start):]
        if ignore_middle and ignore_middle in code:
            code = code.replace(ignore_middle, "")
        return code.strip()

    def find_duplicates(self):
        if not self.file_path:
            messagebox.showerror("Ошибка", "Файл не выбран.")
            return

        ignore_start = self.ignore_start_entry.get().strip()
        try:
            ignore_middle = self.ignore_middle_entry.get().encode().decode("unicode_escape").strip()
        except Exception:
            ignore_middle = ""

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}")
            return

        cleaned = [self.clean_code(line.strip(), ignore_start, ignore_middle) for line in lines]
        seen = set()
        duplicates = set()

        for code in cleaned:
            if code in seen:
                duplicates.add(code)
            else:
                seen.add(code)

        if duplicates:
            output_path = os.path.splitext(self.file_path)[0] + "_duplicates.txt"
            with open(output_path, "w", encoding="utf-8") as f:
                for dup in sorted(duplicates):
                    f.write(dup + "\n")

            messagebox.showinfo("Результат", f"Найдено дублей: {len(duplicates)}\nСохранено в: {output_path}")
        else:
            messagebox.showinfo("Результат", "Дубликатов не найдено.")
