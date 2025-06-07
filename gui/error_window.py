import tkinter as tk
from tkinter import messagebox
from core.error_extractor import ErrorExtractor

class ErrorWindow:
    def __init__(self, root, file_path):
        self.file_path = file_path
        self.window = tk.Toplevel(root)
        self.window.title("Ошибки из лога")
        self.window.geometry("700x500")

        self.text = tk.Text(self.window, wrap=tk.WORD)
        self.text.pack(expand=True, fill=tk.BOTH)

        self.load_errors()

    def load_errors(self):
        extractor = ErrorExtractor(self.file_path)
        errors = extractor.extract_exceptions()

        if not errors:
            self.text.insert(tk.END, "Ошибок не найдено.")
        else:
            for error in errors:
                self.text.insert(tk.END, error + "\n\n")
