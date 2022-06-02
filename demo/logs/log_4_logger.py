import logging
import sys

params = {'level': logging.DEBUG}
if sys.version_info[0] > 3 or sys.version_info[0] == 3 and sys.version_info[1] > 8:
    params['encoding'] = 'utf-8'
logging.basicConfig(**params)
logger = logging.getLogger('myprogram')

logging.debug('my debug 🙄 message')
logging.info('my info message')

logger.warning('my warning ☝ message')
logger.error('my error 😱 message')
