"""
Utilities module.
"""
import os
import re


def get_project_path():
    current_relative_path = os.getcwd()
    split_current_relative_path = current_relative_path.split("\\")
    project_path = ""
    for item in split_current_relative_path:
        project_path += item + "\\\\"
        current_dir_content = os.listdir(project_path)
        if "manage.py" in current_dir_content:
            return project_path


def get_project_path_forward_slash():
    path = get_project_path()
    new_path = re.sub(r"\\\\", "/", path)
    return new_path


if __name__ == "__main__":
    print(get_project_path())
    print(get_project_path_forward_slash())
