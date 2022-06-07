import os
from shutil import rmtree

import pytest
import requests

DOMAIN = 'http://127.0.0.1:8080'


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
    os.chdir(tmpdir)
    files = create_test_files(tmpdir)
    yield files


@pytest.fixture()
def test_file_web(tmpdir):
    requests.post(f'{DOMAIN}/change_dir/{tmpdir}')
    yield create_single_test_file(tmpdir, 'test.txt')


@pytest.fixture()
def test_files_web(tmpdir):
    requests.post(f'{DOMAIN}/change_dir/{tmpdir}')
    files = create_test_files(tmpdir)
    yield files


def create_test_files(folder):
    files = []
    for file_num in (1, 2, 3):
        file_name = f'{file_num}.txt'
        file_path = folder.join(file_name)
        content = b'12345'
        with open(file_path, 'wb') as f:
            f.write(content)
            files.append(file_name)
    return files


def create_single_test_file(folder, filename):
    file = folder.join(filename)
    content = b'12345'
    with open(file, 'wb') as f:
        f.write(content)
    return filename, content
