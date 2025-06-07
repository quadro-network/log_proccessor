import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
import os
from core.km_extractor import KmExtractor


class MassivKMWindow:
    def __init__(self, parent, file_path):
        self.file_path = file_path
        self.window = tk.Toplevel(parent)
        self.window.title("Массив КМ")
        self.window.geometry("400x300")

        tk.Label(self.window, text="С какой даты выгрузить КМ", font=("Arial", 12)).pack(pady=10)

        tk.Label(self.window, text="Выгрузка с начала:").pack()
        self.start_entry = tk.Entry(self.window, width=25)
        self.start_entry.insert(0, "2025-05-07 00:00:00.000")
        self.start_entry.pack(pady=2)

        tk.Label(self.window, text="Выгрузка с конца:").pack()
        self.end_entry = tk.Entry(self.window, width=25)
        self.end_entry.insert(0, "2025-05-07 23:59:59.999")
        self.end_entry.pack(pady=2)

        tk.Button(self.window, text="Готово", bg="#6A5ACD", fg="white",
                  command=self.process).pack(pady=10)

    def process(self):
        try:
            start = self.start_entry.get()
            end = self.end_entry.get()

            # Проверка формата
            start_dt = datetime.strptime(start, "%Y-%m-%d %H:%M:%S.%f")
            end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M:%S.%f")

            # Логика обработки
            extractor = KmExtractor(self.file_path)
            codes = extractor.extract_codes(start_dt, end_dt)


            output_file = "output_codes.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                for code in codes:
                    f.write(code + "\n")

            # Логируем задачу
            data = {}
            path = "selected_tasks.json"
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            data["Массив КМ"] = {
                "start": start,
                "end": end,
                "count": len(codes)
            }

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            messagebox.showinfo("Успех", f"Извлечено {len(codes)} КМ. Результат в {output_file}")
            self.window.destroy()

        except ValueError:
            messagebox.showerror("Ошибка", "Формат даты должен быть: 2025-05-07 00:00:00.000")
