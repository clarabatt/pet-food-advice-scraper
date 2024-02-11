import re
import os


def create_files_directory():
    directory = os.path.join(os.path.abspath("."), "files")
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def get_numbers_from_string(string: str):
    """
    Extracts all numbers from a string and returns them as a list of strings."""
    return re.findall(r"\d+", string)
