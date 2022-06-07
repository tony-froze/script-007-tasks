import os
import time
import logging
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
        msg = f'Invalid directory name: {path}!'
        logging.error(msg)
        raise ValueError(msg)
    try:
        os.chdir(path)
        logging.debug(f'Changing dir to {path}.')
    except FileNotFoundError:
        if autocreate:
            logging.debug(f'Creating dir: {path}.')
            os.makedirs(path, exist_ok=True)
            logging.debug(f'Changing dir to {path}.')
            os.chdir(path)
        else:
            msg = f'There is no such directory "{path}" and autocreate parameter is False.'
            logging.error(msg)
            raise RuntimeError(msg)


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """
    logging.debug('Checking files in work directory')
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
    logging.debug(f'Collecting info about file {filename}.')
    if not pathname_is_valid(filename):
        msg = f'Invalid file name {filename}!'
        logging.error(msg)
        raise ValueError(msg)
    file_info = dict()
    try:
        file_info['name'] = os.path.basename(filename)
        file_info['create_date'] = time.ctime(get_file_creation_time(filename))
        file_info['edit_date'] = time.ctime(os.path.getmtime(filename))
        file_info['size'] = os.path.getsize(filename)
        if verbose:
            file_info['content'] = get_file_content(filename)
        return file_info
    except FileNotFoundError:
        msg = f'There is no such file "{filename}"!'
        logging.error(msg)
        raise RuntimeError(msg)


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
        RuntimeError: if file already exists
    """
    logging.debug(f'Starting file creation {filename}')
    if not pathname_is_valid(filename):
        msg = f'Invalid file name {filename}!'
        logging.error(msg)
        raise ValueError(msg)
    if os.path.exists(filename):
        msg = f'File {filename} already exists!'
        logging.error(msg)
        raise RuntimeError(msg)
    content = content if isinstance(content, bytes) else str.encode(content)
    with open(filename, 'wb') as f:
        f.write(content)
    logging.info(f'File {filename} was created.')
    file_metadata = get_file_data(filename, verbose=True)
    del file_metadata['edit_date']
    return file_metadata


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist or given path isn't a file.
        ValueError: if filename is invalid.
    """

    if not pathname_is_valid(filename):
        msg = f'Invalid file name {filename}!'
        logging.error(msg)
        raise ValueError(msg)
    if not os.path.exists(filename):
        msg = f'There is no such file "{filename}"!'
        logging.error(msg)
        raise RuntimeError(msg)
    if os.path.isfile(filename):
        os.remove(filename)
        logging.info(f'File "{filename}" was removed.')
    else:
        msg = f'The given path "{filename}" is not a file!'
        logging.error(msg)
        raise RuntimeError(msg)
