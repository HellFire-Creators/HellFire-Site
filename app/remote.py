import requests
import json
from flask import current_app, abort

#This thing definitely feels unnecesary and like it could be just one function
class BaseRequestHandler:
    @classmethod
    def request(self, method, url, **kwargs):
        try:
            response = requests.request(method, url, **kwargs)
            self._is_okay(response)
            return self._handle_response(response)
        except Exception as e:
            self._handle_exception(e)
    
    @classmethod
    def _is_okay(self, response: requests.Response):
        if response.ok is not True:
            abort(500)

    @classmethod
    def _handle_response(self, response: requests.Response):
        return response

    @classmethod
    def _handle_exception(self, exception: Exception):
        abort(500)
    

class GithubRequestHandler(BaseRequestHandler):
    @classmethod
    def _handle_response(self, response: requests.Response):
        response_json = json.loads(response.text)
        if 'error' in response_json:
            abort(500)
        return response_json