import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime

TASKS_PATH = "data/tasks.json"
TASK_LOG_PATH = "data/task_log.json"

DEFAULT_TASKS = {
    "Интервал": None,
    "Обрезка по дате": None,
    "Массив КМ": None,
    "Дубли": None,
    "Вывод ошибок": None,
    "Регулярка": None,
    "Прерывание": None,
    "Список методов": None,
    "Json Ответы": None
}

class TaskWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Выбор задач")
        self.window.geometry("300x400")

        self.vars = {}
        tk.Label(self.window, text="Выберите задачи:").pack(pady=10)

        # Чекбоксы
        for task in DEFAULT_TASKS:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.window, text=task, variable=var)
            chk.pack(anchor='w', padx=20)
            self.vars[task] = var

        # Кнопки
        tk.Button(self.window, text="Сохранить", bg="green", fg="white", command=self.save).pack(pady=10)
        tk.Button(self.window, text="Загрузить из файла", command=self.load_from_file).pack(pady=5)

        self.load_existing_tasks()

    def save(self):
        result = {name: (var.get() if var.get() else None) for name, var in self.vars.items()}

        os.makedirs("data", exist_ok=True)
        with open(TASKS_PATH, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        self.log_task_change(result)
        messagebox.showinfo("Готово", "Задачи сохранены.")

    def load_existing_tasks(self):
        if os.path.exists(TASKS_PATH):
            with open(TASKS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for key, value in data.items():
                    if key in self.vars and value is not None:
                        self.vars[key].set(value)

    def load_from_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filepath:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for key, value in data.items():
                        if key in self.vars and value is not None:
                            self.vars[key].set(value)
                    self.log_task_change(data)
                    messagebox.showinfo("Загружено", "Задачи успешно загружены.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")

    def log_task_change(self, data):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "tasks": data
        }

        logs = []
        if os.path.exists(TASK_LOG_PATH):
            with open(TASK_LOG_PATH, "r", encoding="utf-8") as f:
                logs = json.load(f)

        logs.append(log_entry)
        with open(TASK_LOG_PATH, "w", encoding="utf-8") as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)
