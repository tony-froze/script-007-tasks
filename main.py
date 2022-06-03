#!/usr/bin/env python3
import logging

from dotmap import DotMap

from config import config
import server.FileService as fs
from utils.log_utils import create_logs


def main(args: DotMap):
    logging.debug('Start working...')
    fs.change_dir(args.directory)
    fs.create_file('test.txt', '123')
    content = str(fs.get_files()[0].get('content', 'sample data'))
    logging.info(f'Content from file: {content}.')
    fs.delete_file('test.txt')


if __name__ == '__main__':
    create_logs(config.logfile, config.loglevel)
    try:
        main(config)
    except Exception as ex:
        logging.error(f'Unexpected exception occurred: {ex}')
