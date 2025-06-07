from datetime import datetime
import re


class BreakAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def extract_timestamps(self):
        timestamps = []
        with open(self.file_path, "r", encoding="utf-8") as file:
            for line in file:
                if "/plc/product" in line:
                    try:
                        ts = datetime.strptime(line[:23], "%Y-%m-%d %H:%M:%S.%f")
                        timestamps.append(ts)
                    except:
                        continue
        return timestamps

    def find_breaks(self, min_diff_sec: int):
        result = []
        timestamps = self.extract_timestamps()
        threshold = min_diff_sec  # секундами

        for i in range(1, len(timestamps)):
            delta = timestamps[i] - timestamps[i - 1]
            if delta.total_seconds() >= threshold:
                result.append(
                    f"{delta} между {timestamps[i - 1].time()} и {timestamps[i].time()}"
                )
        return result
