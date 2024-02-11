import os
import json
import logging
from datetime import date
from utils.others import create_files_directory


def load_or_initialize_json_file(file_path):
    """
    Loads JSON data from a file if it exists, or initializes a new structure if it does not.
    """
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    return {"metadata": {}, "data": {}}


def append_data_to_json_file(
    data: dict, description: str, session_code: int, file_name: str
):
    """
    Appends the data to a JSON file. If the file doesn't exist, it creates a new one.
    """
    try:
        file_path = save_data_to_json_file(data, description, file_name, session_code)
        logging.info(f"Data successfully saved to {file_path}")
    except Exception as e:
        logging.error(f"Error saving data to JSON: {e}")


def save_data_to_json_file(
    data: dict, description: str, file_name: str, session_code: int = 1111
):
    """
    Saves data into a JSON file in a specified directory. Creates the file or appends to it if it exists.
    """
    directory = create_files_directory()

    file_path = os.path.join(
        directory, f"{date.today()}_{session_code}_{file_name}.json"
    )
    existing_data = load_or_initialize_json_file(file_path)

    data_key = next(iter(data))
    num_items = len(data[data_key])
    existing_data["metadata"].setdefault("extraction_date", str(date.today()))
    existing_data["metadata"].setdefault("total_items", 0)
    existing_data["metadata"].setdefault("description", description)
    existing_data["metadata"]["total_items"] += num_items

    existing_data["data"].update(data)

    with open(file_path, "w") as file:
        json.dump(existing_data, file)

    return file_path
