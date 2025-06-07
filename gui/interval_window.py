import tkinter as tk
from tkinter import messagebox
from core.interval_analyzer import IntervalAnalyzer
import os


class IntervalWindow:
    def __init__(self, parent, file_path):
        self.file_path = file_path
        self.window = tk.Toplevel(parent)
        self.window.title("Интервал")
        self.window.geometry("400x300")

        tk.Label(self.window, text=f"Добавленный файл:\n{os.path.basename(file_path)}", font=("Arial", 10)).pack(pady=5)

        tk.Label(self.window, text="Массив времени", fg="#6A5ACD", font=("Arial", 10, "bold")).pack()

        tk.Label(self.window, text="Указать интервал (ms):").pack()
        self.interval_entry = tk.Entry(self.window)
        self.interval_entry.insert(0, "30")  # по умолчанию 30 ms
        self.interval_entry.pack(pady=5)

        tk.Button(self.window, text="Сохранить результат", bg="gray", fg="white",
                  command=self.analyze).pack(pady=10)

        self.output_text = tk.Text(self.window, height=10, wrap=tk.WORD)
        self.output_text.pack(expand=True, fill="both", padx=10)

    def analyze(self):
        try:
            max_diff = int(self.interval_entry.get())
            analyzer = IntervalAnalyzer(self.file_path)
            results = analyzer.find_short_intervals(max_diff)

            output = f"Промежутки меньше 0:00:00.{max_diff:03d}000:\n"
            output += "\n".join(results) if results else "Нет подходящих интервалов."
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, output)

            with open("interval_result.txt", "w", encoding="utf-8") as f:
                f.write(output)

            messagebox.showinfo("Готово", "Результат сохранён в interval_result.txt")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное число в миллисекундах.")
