import os
import json

import pytest
import requests


DOMAIN = 'http://127.0.0.1:8080'


@pytest.mark.parametrize('bad_dir',
                         ['NEW:DIR',
                          os.path.join('dir..', 'to', 'go')]
                         )
def test_change_dir_error(bad_dir):
    response = requests.post(f'{DOMAIN}/change_dir/{bad_dir}')
    assert response.status_code == 200
    assert 'Invalid' in response.text


def test_change_dir_success(tmpdir):
    response = requests.post(f'{DOMAIN}/change_dir/{tmpdir}')
    assert response.status_code == 200
    assert 'success' in response.text


def test_get_files(test_files_web):
    response = requests.get(f'{DOMAIN}/files')
    assert response.status_code == 200
    pretty_response = json.loads(response.text)
    assert pretty_response['files'][0]['name'] == test_files_web[0]


def test_get_file_data(test_file_web):
    response = requests.get(f'{DOMAIN}/{test_file_web[0]}')
    assert response.status_code == 200
    pretty_response = json.loads(response.text)
    assert pretty_response['name'] == test_file_web[0]


def test_create_dir(tmpdir):
    requests.post(f'{DOMAIN}/change_dir/{tmpdir}')
    headers = {'Content-type': 'text/html'}
    content = '123asdячс'
    filename = 'test.txt'
    response = requests.post(f'{DOMAIN}/create/{filename}',
                             data=content.encode('utf-8'),
                             headers=headers)
    assert response.status_code == 200
    pretty_response = json.loads(response.text)
    assert pretty_response['content'] == content


def test_delete_file(test_file_web):
    response = requests.delete(f'{DOMAIN}/delete/{test_file_web[0]}')
    assert response.status_code == 200
    pretty_response = json.loads(response.text)
    assert 'location' in pretty_response



