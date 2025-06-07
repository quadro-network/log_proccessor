import tkinter as tk
from tkinter import messagebox, StringVar
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

from core.trim_controller import TrimController  # добавлено


class TrimDateWindow:
    def __init__(self, parent, file_path):
        self.file_path = file_path
        self.window = tk.Toplevel(parent)
        self.window.title("Обрезка по дате")
        self.window.geometry("400x300")

        tk.Label(self.window, text="С какой даты обрезать до конца файла", font=("Arial", 12)).pack(pady=10)

        tk.Label(self.window, text="Обрезка с начала:").pack()

        self.start_date_var = StringVar()
        self.start_date = DateEntry(self.window, textvariable=self.start_date_var,
                                    date_pattern='yyyy-mm-dd', state='normal')
        self.start_date.pack(pady=2)
        self.start_date.bind("<Control-v>", self.paste_date)

        self.start_time = tk.Entry(self.window, width=20)
        self.start_time.insert(0, "00:00:00.000")
        self.start_time.pack(pady=2)

        tk.Label(self.window, text="Обрезка с конца:").pack()

        self.end_date_var = StringVar()
        self.end_date = DateEntry(self.window, textvariable=self.end_date_var,
                                  date_pattern='yyyy-mm-dd', state='normal')
        self.end_date.pack(pady=2)
        self.end_date.bind("<Control-v>", self.paste_date)

        self.end_time = tk.Entry(self.window, width=20)
        self.end_time.insert(0, "23:59:59.999")
        self.end_time.pack(pady=2)

        tk.Button(self.window, text="Готово", bg="#6A5ACD", fg="white",
                  command=self.process_trim).pack(pady=10)

    def paste_date(self, event):
        try:
            clipboard = self.window.clipboard_get().strip()
            date_str = clipboard.split()[0]
            datetime.strptime(date_str, "%Y-%m-%d")
            event.widget.delete(0, tk.END)
            event.widget.insert(0, date_str)
        except Exception:
            messagebox.showwarning("Ошибка", "Буфер не содержит корректную дату в формате YYYY-MM-DD.")

    def process_trim(self):
        try:
            start = f"{self.start_date.get()} {self.start_time.get()}"
            end = f"{self.end_date.get()} {self.end_time.get()}"

            datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
            datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")

            # Сохраняем параметры в selected_tasks.json
            path = "selected_tasks.json"
            data = {}
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            data["Обрезка по дате"] = {"start": start, "end": end}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # Запускаем обработку лог-файла
            controller = TrimController(self.file_path)
            output_file = "output_trimmed.log"
            controller.trim_between(start, end, output_file)

            messagebox.showinfo("Успех", f"Результат сохранён в {output_file}")
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат времени. Пример: 21:16:28.643")
