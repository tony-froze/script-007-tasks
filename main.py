#!/usr/bin/env python3
import logging

from aiohttp import web

from server.WebHandler import WebHandler

from config import config
from utils.log_utils import create_logs


def main():
    logging.debug('Start working...')
    logging.debug(f'Ready to listen to port {config.port}.')
    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.post('/change_dir/{path:.+}', handler.change_dir),
        web.get('/files', handler.get_files),
        web.get('/{filename}', handler.get_file_data),
        web.post('/create/{filename}', handler.create_file),
        web.delete('/delete/{filename}', handler.delete_file,)
        # TODO: add more routes
    ])
    web.run_app(app, port=config.port)


if __name__ == '__main__':
    create_logs(config.logfile, config.loglevel)
    try:
        main()
    except Exception as ex:
        logging.error(f'Unexpected exception occurred: {ex}')
