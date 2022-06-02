import logging
import sys

params = {'filename': 'myapp.log', 'level': logging.DEBUG}
if sys.version_info[0] > 3 or sys.version_info[0] == 3 and sys.version_info[1] > 8:
    params['encoding'] = 'utf-8'
logging.basicConfig(**params)

logging.debug('my debug 🙄 message')
logging.info('my info message')
logging.warning('my warning ☝ message')
logging.error('my error 😱 message')
