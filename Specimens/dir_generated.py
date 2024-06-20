
# your_script.py

import os

def get_directory_contents(directory_path):
    return [file_name for file_name in os.listdir(directory_path)]
