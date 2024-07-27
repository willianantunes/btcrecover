import pathlib
import shutil
import uuid

from contextlib import contextmanager
from typing import List


@contextmanager
def create_structure(structure: dict, current_folder=None, folder_name=None, delete_files=True) -> List[str]:
    created_files = []

    try:
        for index, (file_or_new_structure, content) in enumerate(structure.items()):
            if index == 0:
                if not current_folder:
                    folder_name = f"./tmp-{uuid.uuid4()}"
                else:
                    folder_name = f"{current_folder}/{folder_name}"
                current_folder = create_dir_if_not_exist_returning_abs_path(folder_name)
            is_file = isinstance(content, str)
            if is_file:
                file_path = f"{current_folder}/{file_or_new_structure}"
                created_file_path = create_file_with_content(file_path, content)
                created_files.append(created_file_path)
            else:
                with create_structure(
                    content, current_folder=current_folder, folder_name=file_or_new_structure, delete_files=False
                ) as (_, new_created_files):
                    created_files += new_created_files

        yield current_folder, created_files
    finally:
        if delete_files:
            if created_files:
                for file in created_files:
                    file.unlink()
            shutil.rmtree(current_folder)


def create_file_with_content(file_path, content):
    file_path = pathlib.Path(file_path)

    with open(file_path, mode="a") as file:
        file.writelines(content)

    return file_path


def create_dir_if_not_exist_returning_abs_path(dir_name: str):
    folder_path = pathlib.Path(dir_name)
    pathlib.Path(dir_name).mkdir(exist_ok=True)

    return folder_path.resolve()


def load_content_as_string(file_name) -> str:
    with open(file_name, mode="r") as file:
        return file.read()
