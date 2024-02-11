import re
import os
import json
from datetime import date


def get_numbers_from_string(string: str):
    """
    Params: string: str
    Returns: List[str]
    Extracts all numbers from a string and returns them as a list of strings."""
    return re.findall(r"\d+", string)


def save_to_json_into_files(data: any, file_name: str, execution_code: str = "1111"):
    """
    Params: data: any, file_name: str, execution_code: str
    Returns: str (path to the file created)
    Saves the data into a json file in the files folder with the given file_name and execution_code. If the file doesn't exist, it creates it.
    """
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    directory = os.path.join(root, "files")
    if not os.path.exists(directory):
        os.makedirs(directory)

    path = f"{directory}/{date.today()}_{execution_code}_{file_name}.json"

    existing_data = []
    if os.path.exists(path):
        with open(path, "r") as file:
            existing_data = json.load(file)

    data_object = json.loads(data)
    existing_data.append(data_object)

    with open(path, "w") as file:
        json.dump(existing_data, file)

    return path
