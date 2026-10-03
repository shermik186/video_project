from schemas import MovieInput, MoviesInput
from crud import create_set_of_relative_pathes

from pathlib import Path
from dotenv import load_dotenv


import os


def get_root():
    load_dotenv()
    server = os.getenv("SERVER_URL")
    root = Path(server)
    return root


def scan_new_relative_paths():
    root = get_root()
    suffix_set = {".mkv", ".mp4", ".avi", ".mpg"}
    existing_paths = create_set_of_relative_pathes()
    new_paths = []
    for relative_path in root.rglob("*"):
        if relative_path.suffix.lower() in suffix_set:
            rel_path = str(relative_path.relative_to(root))
            if rel_path not in existing_paths:
                new_paths.append(rel_path)

    print(f"Nalezeno nových cest v hledaci funkci: {len(new_paths)}")
    return new_paths


def get_paths():
    paths_list = scan_new_relative_paths()
    return paths_list


def turn_list_to_text(arr):
    arr_text = ", ".join(arr)
    return arr_text


def create_testing_data():
    root = get_root()
    suffix_set = {".mkv", ".mp4", ".avi", ".mpg"}
    new_paths = []
    count = 0
    for relative_path in root.rglob("*"):
        if relative_path.suffix in suffix_set:
            rel_path = str(relative_path.relative_to(root))
            new_paths.append(rel_path)
            count += 1
            if count == 20:
                return new_paths


def print_files():
    root = get_root()
    for file in root.rglob("*"):
        print(file.relative_to(root))
