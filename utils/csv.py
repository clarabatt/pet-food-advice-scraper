import os
import csv
from datetime import date
from utils.others import create_files_directory


def append_to_csv(json_data: dict, file_name: str):
    """
    Converts JSON data and append into a CSV file.
    """
    directory = create_files_directory()

    file_path = os.path.join(directory, f"{date.today()}_{file_name}.csv")

    processed_data = {k: v for d in json_data.values() for k, v in d.items()}

    if isinstance(processed_data, dict):
        processed_data = [processed_data]

    with open(file_path, "a", newline="", encoding="utf-8") as file:
        if os.stat(file_path).st_size == 0:
            # File is empty, write header
            writer = csv.DictWriter(file, fieldnames=processed_data[0].keys())
            writer.writeheader()
        else:
            writer = csv.DictWriter(file, fieldnames=processed_data[0].keys())

        writer.writerows(processed_data)
