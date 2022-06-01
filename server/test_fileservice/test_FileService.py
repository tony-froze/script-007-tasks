import os

import pytest

from server.FileService import (change_dir,
                                create_file,
                                delete_file,
                                get_file_data,
                                get_files)


class TestChangeDir:
    @pytest.mark.parametrize('bad_dir',
                             ['NEW:DIR',
                              os.path.join('dir..', 'to', 'go')]
                             )
    def test_change_dir_value_error(self, bad_dir):
        with pytest.raises(ValueError):
            change_dir(bad_dir)

    def test_change_dir_to_not_exists_without_autocreate(self, not_existed_dir):
        with pytest.raises(RuntimeError):
            change_dir(not_existed_dir, False)

    def test_change_dir_to_not_exists_autocreate(self, not_existed_dir):
        change_dir(not_existed_dir, True)
        assert os.getcwd().split(os.path.sep)[-1] == not_existed_dir

    def test_change_dir_ok(self, existed_dir):
        change_dir(existed_dir)
        assert os.getcwd() == existed_dir


class TestGetFileData:
    @pytest.mark.parametrize('bad_name',
                             ['bad:name.txt',
                              os.path.join('dir', 'to', 'go', '*too_bad_name*.zxc')]
                             )
    def test_get_file_data_value_error(self, bad_name):
        with pytest.raises(ValueError):
            get_file_data(bad_name)

    def test_get_file_data_runtime_error(self, tmpdir):
        file = tmpdir.join('not_existed_file.txt')
        with pytest.raises(RuntimeError):
            get_file_data(str(file))

    def test_get_file_data_return_type(self, test_file):
        assert isinstance(get_file_data(test_file[0]), dict)

    def test_get_file_data_return_content(self, test_file):
        file_data = get_file_data(test_file[0], verbose=True)
        assert file_data['content'] == test_file[1]

    def test_get_file_data_return_keys(self, test_file):
        file_data = get_file_data(test_file[0], verbose=False)
        expected_keys = ('name', 'create_date', 'edit_date', 'size')
        real_keys = file_data.keys()
        assert all(key in real_keys for key in expected_keys) and len(real_keys) == 4


class TestGetFiles:
    def test_get_files_data_empty(self, tmpdir):
        os.chdir(tmpdir)
        assert get_files() == []

    def test_get_files_data_len(self, test_files):
        assert len(get_files()) == len(test_files)

    def test_get_files_data_names(self, test_files):
        read_file_names = sorted([file['name'] for file in get_files()])
        assert read_file_names == test_files


class TestCreateFile:
    @pytest.mark.parametrize('bad_name',
                             ['bad:name.txt',
                              os.path.join('dir', 'to', 'go', '*too_bad_name*.zxc')]
                             )
    def test_create_file_bad_name(self, bad_name):
        with pytest.raises(ValueError):
            create_file(bad_name, '123')

    def test_create_file_already_exists(self, test_file):
        with pytest.raises(RuntimeError):
            create_file(test_file[0], b'new_content')

    def test_created_file_exists(self, tmpdir):
        file = tmpdir.join('test_file.txt')
        create_file(str(file), b'12345')
        assert file.exists()

    def test_create_file_return_type(self, tmpdir):
        file = tmpdir.join('test_file.txt')
        new_file_data = create_file(str(file), b'12345')
        assert isinstance(new_file_data, dict)

    def test_create_file_content(self, tmpdir):
        file = tmpdir.join('test_file.txt')
        content = b'12345'
        new_file_data = create_file(str(file), content)
        assert new_file_data['content'] == content

    def test_create_file_return_keys(self, tmpdir):
        file = tmpdir.join('test_file.txt')
        new_file_data = create_file(str(file), b'12345')
        expected_keys = ('name', 'create_date', 'content', 'size')
        real_keys = new_file_data.keys()
        assert all(key in real_keys for key in expected_keys) and len(real_keys) == 4


class TestDeleteFile:
    pass
