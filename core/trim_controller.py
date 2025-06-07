from datetime import datetime


class TrimController:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _parse_timestamp(self, line: str) -> datetime | None:
        try:
            return datetime.strptime(line[:23], "%Y-%m-%d %H:%M:%S.%f")
        except:
            return None

    def trim_from_start(self, start_datetime: str, output_path: str):
        """Обрезает от указанной даты до конца"""
        start = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S.%f")
        with open(self.file_path, "r", encoding="utf-8") as infile, \
             open(output_path, "w", encoding="utf-8") as outfile:
            writing = False
            for line in infile:
                dt = self._parse_timestamp(line)
                if dt and dt >= start:
                    writing = True
                if writing:
                    outfile.write(line)

    def trim_to_end(self, end_datetime: str, output_path: str):
        """Обрезает от начала до указанной даты"""
        end = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S.%f")
        with open(self.file_path, "r", encoding="utf-8") as infile, \
             open(output_path, "w", encoding="utf-8") as outfile:
            for line in infile:
                dt = self._parse_timestamp(line)
                if dt and dt > end:
                    break
                outfile.write(line)

    def trim_between(self, start_str: str, end_str: str, output_path: str):
        """Обрезает только между двумя датами"""
        start = datetime.strptime(start_str, "%Y-%m-%d %H:%M:%S.%f")
        end = datetime.strptime(end_str, "%Y-%m-%d %H:%M:%S.%f")
        with open(self.file_path, "r", encoding="utf-8") as infile, \
             open(output_path, "w", encoding="utf-8") as outfile:
            for line in infile:
                dt = self._parse_timestamp(line)
                if dt and start <= dt <= end:
                    outfile.write(line)
