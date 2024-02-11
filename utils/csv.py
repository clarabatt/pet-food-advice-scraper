import os
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

    if os.path.exists(directory):
        with open(file_path, "a") as file:
            for key, value in json_data.items():
                file.write(f"{key},{value}\n")
