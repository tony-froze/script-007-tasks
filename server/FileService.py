import os
import datetime
from typing import Union

from utils.file_utils import get_file_content, get_file_creation_time, pathname_is_valid


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """
    if not pathname_is_valid(path):
        raise ValueError(f'Invalid directory name: {path}!')
    try:
        os.chdir(path)
    except FileNotFoundError:
        if autocreate:
            os.makedirs(path, exist_ok=True)
            os.chdir(path)
        else:
            raise RuntimeError(f'There is no such directory "{path}" and autocreate parameter is False.')


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """

    files = os.listdir()
    return [get_file_data(file) for file in files]


def get_file_data(filename: str, verbose: bool = False) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.
        verbose (bool): Get file content in addition to other info.

    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """
    if not pathname_is_valid(filename):
        raise ValueError(f'Invalid file name {filename}!')
    file_info = dict()
    try:
        file_info['name'] = os.path.basename(filename)
        file_info['create_date'] = datetime.datetime.fromtimestamp(get_file_creation_time(filename))
        file_info['edit_date'] = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        file_info['size'] = os.path.getsize(filename)
        if verbose:
            file_info['content'] = get_file_content(filename)
        return file_info
    except FileNotFoundError:
        raise RuntimeError(f'There is no such file "{filename}"!')


def create_file(filename: str, content: Union[str, bytes]) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """

    if not pathname_is_valid(filename):
        raise ValueError(f'Invalid file name: {filename}!')
    if os.path.exists(filename):
        raise RuntimeError(f'File {filename} already exists!')
    with open(filename, 'wb') as f:
        f.write(str.encode(content))
    file_metadata = get_file_data(filename,verbose=True)
    del file_metadata['edit_date']
    return file_metadata


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """

    if not pathname_is_valid(filename):
        raise ValueError(f'Invalid file name: {filename}!')
    if not os.path.exists(filename):
        raise RuntimeError(f'There is no such file "{filename}"!')
    if os.path.isfile(filename):
        os.remove(filename)
    else:
        raise RuntimeError(f'The given path "{filename}" is not a file!')
