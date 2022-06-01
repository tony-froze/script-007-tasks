import os

import pytest

from server.FileService import change_dir


def test_change_dir_value_error():
    for param in ['NEW:DIR', os.path.join('dir..', 'to', 'go')]:
        with pytest.raises(ValueError):
            change_dir(param)


def test_change_dir_to_not_exists():
    with pytest.raises(RuntimeError):
        change_dir('not_existed_dir', False)


def test_change_dir_autocreate():
    dir_name = 'not_existed_dir'
    change_dir(dir_name, True)
    assert os.getcwd().split(os.path.sep)[-1] == dir_name


def test_change_dir_ok():
    dir_name = 'existed_dir'
    os.mkdir(dir_name)
    change_dir(dir_name)
    assert os.getcwd().split(os.path.sep)[-1] == dir_name

