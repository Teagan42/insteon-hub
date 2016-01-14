from urllib.parse import urlencode
import json
import sys
import requests

API_URL = "https://connect.insteon.com"

class APIError(Exception):
    """API Error Response

    Attributes:
        msg -- the error message
        code -- the error code
    """
    def __init__(self, data):
        self.data = data

class InsteonAPI(object):
    def __init__(self, authorizer, client_id, user_agent):
        self.authorizer = authorizer
        self.user_agent = user_agent
        self.client_id = client_id

    def get(self, path, parameters = ''):
        '''Perform GET Request'''

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            path += '?' + parameter_string

        response = requests.get(API_URL + path, headers=self._set_headers())
        return self._check_response(response)

    def post(self, path, data={}):
        '''Perform POST Request '''

        response = requests.post(API_URL + path, data=json.dumps(data), headers=self._set_headers())
        return self._check_response(response)

    def put(self, path, data={}):
        '''Perform PUT Request'''
        response = requests.put(API_URL + path, data=json.dumps(data), headers=setup_headers())
        return self._check_response(response)

    def delete(self, path, parameters={}):
        '''Perform GET Request'''

        if parameters != '':
            parameter_string = ''
            for k,v in parameters.items():
                parameter_string += '{}={}'.format(k,v)
                parameter_string += '&'
            path += '?' + parameter_string

        response = requests.delete(API_URL + path, headers=self._set_headers())
        return self._check_response(response)

    def _check_response(self, response):
        if response.status_code >= 400:
            raise APIError(data)

        if response.status_code == 204:
            return True

        return response.json()

    def _set_headers(self):
        return {
                "Content-Type": "application/json",
                "Authentication": "APIKey " + self.client_id,
                "Authorization": "Bearer " + self.authorizer.access_token
            }

    @classmethod
    def unauth_post(cls, path, data):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = requests.post(API_URL + '/api/v2/oauth2/token', data=data, headers=headers)
        return response.json()