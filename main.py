#!/usr/bin/env python3
import logging

from dotmap import DotMap
from aiohttp import web

from server.WebHandler import WebHandler as wh

from config import config
import server.FileService as fs
from utils.log_utils import create_logs


def main(args: DotMap):
    logging.debug('Start working...')
    logging.debug(f'Ready to listen to port {config.port}.')
    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        # TODO: add more routes
    ])
    web.run_app(app, port=config.port)
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
