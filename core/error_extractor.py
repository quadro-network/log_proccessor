import re

class ErrorExtractor:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_exceptions(self):
        errors = []
        collect = False
        current_error = []

        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                if "Exception" in line or "Unhandled" in line or "stack trace" in line:
                    collect = True

                if collect:
                    current_error.append(line.strip())
                    if line.strip() == "" or line.startswith("202"):
                        # Конец блока или начало новой записи
                        errors.append("\n".join(current_error).strip())
                        current_error = []
                        collect = False

        return [e for e in errors if e]
