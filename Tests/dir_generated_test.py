import os
import pytest
from Specimens.dir_generated import get_directory_contents  # replace 'your_script' with your script name

@pytest.mark.parametrize("dir_path", ["/path/to/directory1", "/path/to/directory2"])
def test_get_directory_contents(dir_path):
    dir_list = get_directory_contents(dir_path)  # call your function
    expected_list = os.listdir(dir_path)  # use Python's built-in listdir function
    assert set(dir_list) == set(expected_list)
