import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from gui.trim_date_window import TrimDateWindow
from gui.interval_window import IntervalWindow
from gui.break_window import BreakWindow
from gui.error_window import ErrorWindow
from gui.duplicates_window import DuplicatesWindow
from gui.regex_window import RegexSearchWindow

import os
import json



class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Log Processor")
        self.root.geometry("500x260")
        self.file_path = None

        self.label = tk.Label(root, text="Файл не загружен", font=("Arial", 12), fg="gray")
        self.label.pack(pady=10)

        tk.Button(root, text="Загрузка лога", bg="#6A5ACD", fg="white",
                  command=self.load_file, width=20, height=2).pack()

        self.method_names = self.load_method_names("config/methods.json")
        self.create_method_buttons(root)


    def load_method_names(self, json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Ошибка загрузки", f"Не удалось загрузить методы: {e}")
            return []

    def create_method_buttons(self, parent):
        frame = tk.Frame(parent)
        frame.pack(pady=20)

        for i, name in enumerate(self.method_names):
            command = self.get_method_callback(name)
            btn = tk.Button(frame, text=name, bg="orange", width=18, height=2, command=command)
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def get_method_callback(self, name):
        if name == "Обрезка по дате":
            return self.open_trim_window
        elif name == "Интервал":
            return self.open_interval_window
        elif name == "Прерывание":
            return self.open_break_window
        elif name == "Массив КМ":
            return self.open_massiv_km_window
        elif name == "Вывод ошибок":
            return self.open_error_window
        elif name == "Регулярка":
            return self.open_regex_window
        elif name == "Дубли":
            return self.open_duplicates_window


        else:
            return self.not_implemented

    def load_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Log files", "*.log"), ("All files", "*.*")])
        if filepath:
            self.file_path = filepath
            self.label.config(text=f"Загружен: {os.path.basename(filepath)}", fg="black")
        else:
            self.label.config(text="Файл не загружен", fg="gray")
    def open_error_window(self):
        if not self.file_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите лог-файл.")
            return
        ErrorWindow(self.root, self.file_path)




    def save_file(self):
        if not self.file_path:
            messagebox.showwarning("Сначала загрузите файл", "Файл не выбран")
            return

        filename = simpledialog.askstring("Имя файла", "Введите имя (без расширения):")
        if filename:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                initialfile=f"{filename}.txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if save_path:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write("Пример результата обработки.\n")
                messagebox.showinfo("Сохранено", f"Файл сохранён: {save_path}")
    def open_regex_window(self):
        if not self.file_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите лог-файл.")
            return
        RegexSearchWindow(self.root, self.file_path)


    def open_trim_window(self):
        if not self.file_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите лог-файл.")
            return
        TrimDateWindow(self.root, self.file_path)

    def open_interval_window(self):
        if not self.file_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите лог-файл.")
            return
        IntervalWindow(self.root, self.file_path)

    def open_break_window(self):
        if not self.file_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите лог-файл.")
            return
        BreakWindow(self.root, self.file_path)

 

    def open_duplicates_window(self):
        if not self.file_path:
            messagebox.showwarning("Ошибка", "Сначала загрузите лог-файл.")
            return
        DuplicatesWindow(self.root)



    def not_implemented(self):
        messagebox.showinfo("Инфо", "Функция пока не реализована.")
