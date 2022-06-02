#!/usr/bin/env python3
import argparse
import os
import logging

import server.FileService as fs
from utils.log_utils import create_logs


def main(args: argparse.Namespace):
    logging.debug('Start working...')
    fs.change_dir(args.directory)
    fs.create_file('test.txt', '123')
    content = str(fs.get_files()[0].get('content', 'sample data'))
    logging.info(f'Content from file: {content}.')
    fs.delete_file('test.txt')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, required=True, help="Working directory")
    parser.add_argument('-l', '--loglevel',  type=str, default='INFO',
                        choices=logging._nameToLevel.keys(), help="Logging level")
    parser.add_argument('-f', '--logfile',  type=str, default='server.log',  help="Logging file")
    arguments = parser.parse_args()
    create_logs(arguments.logfile, arguments.loglevel)
    main(arguments)
