import os
import csv
from datetime import date
from utils.others import create_files_directory


def append_to_csv(json_data: dict, session_code: int, file_name: str):
    """
    Converts JSON data and append into a CSV file.
    """
    directory = create_files_directory()

    file_path = os.path.join(
        directory, f"{date.today()}_{session_code}_{file_name}.csv"
    )

    merged = {k: v for d in json_data.values() for k, v in d.items()}

    if os.path.exists(directory):
        with open(file_path, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=merged.keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(merged)
