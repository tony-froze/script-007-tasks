import logging
import os.path

from aiohttp import web

import server.FileService as FileService


class WebHandler:
    """aiohttp handler with coroutines."""

    async def handle(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Basic coroutine for connection testing.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with status.
        """

        return web.json_response(data={
            'status': 'success',
            'curr_dir': os.getcwd(),
        })

    async def change_dir(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for changing working directory with files.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                "path": "string. Directory path. Required",
            }.

        Returns:
            Response: JSON response with success status and success message or error status and error message.
        """
        try:
            path = request.match_info.get('path', 'new_data')
            logging.info(f'Received path: {path}')
            autocreate = False if request.query.get('autocreate', '').lower() == 'false' else True
            FileService.change_dir(os.path.abspath(path), autocreate=autocreate)
            data = {
                    'status': 'success',
                    'message': f'The current directory has been successfully changed to "{os.getcwd()}".'
            }
        except (RuntimeError, ValueError) as ex:
            data = {
                    'status': 'error',
                    'message': str(ex),
                    'operation': 'changing directory'
            }
        except Exception as ex:
            logging.error(f'Unexpected exception {str(ex)}.')
            data = {'status': 'fatal error', }
        return self.construct_response(data)

    async def get_files(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting info about all files in working directory.

        Args:
            request (Request): aiohttp request.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """
        try:
            data = {'status': 'success'}
            data.update({'files': FileService.get_files()})
        except (RuntimeError, ValueError) as ex:
            data = {'status': 'error', 'message': str(ex), 'operation': 'collecting files data'}
        except Exception as ex:
            logging.error(f'Unexpected exception {str(ex)}.')
            data = {'status': 'fatal error', }
        return self.construct_response(data)

    async def get_file_data(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for getting full info about file in working directory.

        Args:
            request (Request): aiohttp request, contains filename and is_signed parameters.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """
        try:
            filename = request.match_info.get('filename', '')
            data = {'status': 'success'}
            data.update(FileService.get_file_data(filename, verbose=True))
        except (RuntimeError, ValueError) as ex:
            data = {'status': 'error', 'message': str(ex), 'operation': 'getting file data'}
        except Exception as ex:
            logging.error(f'Unexpected exception {str(ex)}.')
            data = {'status': 'fatal error', }
        return self.construct_response(data)

    async def create_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for creating file.

        Args:
            request (Request): aiohttp request, contains JSON in body. JSON format:
            {
                'filename': 'string. filename',
                'content': 'string. Content string. Optional',
            }.

        Returns:
            Response: JSON response with success status and data or error status and error message.
        """
        try:
            filename = request.match_info.get('filename', '')
            content = await request.read()
            data = {'status': 'success'}
            data.update(FileService.create_file(filename, content))
        except (RuntimeError, ValueError) as ex:
            data = {'status': 'error', 'message': str(ex), 'operation': 'creating file'}
        except Exception as ex:
            logging.error(f'Unexpected exception {str(ex)}.')
            data = {'status': 'fatal error', }
        return self.construct_response(data)

    async def delete_file(self, request: web.Request, *args, **kwargs) -> web.Response:
        """Coroutine for deleting file.

        Args:
            request (Request): aiohttp request, contains filename.

        Returns:
            Response: JSON response with success status and success message or error status and error message.
        """
        try:
            filename = request.match_info.get('filename', '')
            data = {'status': 'success', 'location': os.path.join(os.getcwd(), filename)}
            FileService.delete_file(filename)
        except (RuntimeError, ValueError) as ex:
            data = {'status': 'error', 'message': str(ex), 'operation': 'deleting file'}
        except Exception as ex:
            logging.error(f'Unexpected exception {str(ex)}.')
            data = {'status': 'fatal error', }
        return self.construct_response(data)

    @staticmethod
    def construct_response(data: dict):
        if data['status'] == 'error':
            data['message'] = f'Error "{data["message"]}" has occurred when {data["operation"]}.'
            del data["operation"]
        elif data['status'] == 'fatal_error':
            data['message'] = f'Unexpected error has occurred. Please contact tech support.'
        return web.json_response(data)
