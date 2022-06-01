import os
from shutil import rmtree

import pytest


@pytest.fixture()
def not_existed_dir():
    current_folder = os.getcwd()
    dir_name = 'not_existed_dir'
    check_and_remove_dir(dir_name)
    yield dir_name
    os.chdir(current_folder)
    check_and_remove_dir(dir_name)


def check_and_remove_dir(dir_name):
    full_path = os.path.join(os.getcwd(), dir_name)
    if os.path.isdir(full_path):
        rmtree(full_path, ignore_errors=True)


@pytest.fixture()
def existed_dir():
    current_folder = os.getcwd()
    dir_name = create_unique_test_dir(current_folder)
    yield dir_name
    os.chdir(current_folder)
    rmtree(dir_name, ignore_errors=True)


def create_unique_test_dir(current_folder):
    dir_name = 'existed_dir'
    while True:
        full_path = os.path.join(current_folder, dir_name)
        if os.path.isdir(full_path):
            dir_name += '1'
            continue
        os.mkdir(full_path)
        return full_path


@pytest.fixture()
def test_file(tmpdir):
    file = tmpdir.join('test.txt')
    content = b'12345'
    with open(file, 'wb') as f:
        f.write(content)
    yield str(os.path.normpath(file)), content


@pytest.fixture()
def test_files(tmpdir):
    files = []
    for file_num in (1, 2, 3):
        file_name = f'{file_num}.txt'
        file_path = tmpdir.join(file_name)
        content = b'12345'
        with open(file_path, 'wb') as f:
            f.write(content)
            files.append(file_name)
    os.chdir(tmpdir)
    return files
