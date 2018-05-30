import requests
import json
from typing import Dict


class VKRequest:
    def __init__(self):
        with open('..\\access_token.txt') as file:
            self.access_token = file.read()
        self.version = json.load(open('..\config.json'))['version']

    def get_url(self, method_name: str, parameters: str) -> str:
        """
        Includes method and parameters in the URL
        :param method_name: string of VK API method
        :param parameters: dictionary of parameters and it's values, access token and version already included
        :return: string with correct for VK API URL
        """
        return f'https://api.vk.com/method/{method_name}?{parameters}&access_token={self.access_token}&v={self.version}'

    @staticmethod
    def combine_params(parameters: Dict[str, str]) -> str:
        """
        Connects parameters to an ampersand to send a request
        :param parameters: dictionary of parameters and it's values from VK API method to join, access token and
        version already included
        :return: string with ampersand-connected parameters
        """
        return '&'.join([f'{key}={parameters[key]}' for key in parameters])

    def get(self, method_name: str, parameters: Dict[str, str]) -> json:
        """
        Makes GET request containing data necessary for VK API
        :param method_name: string of VK API method
        :param parameters: dictionary of parameters and it's values, access token and version already included
        :return: json response from VK API
        """
        return requests.get(self.get_url(method_name, self.combine_params(parameters))).json()

    def post(self, method_name: str, parameters: Dict[str, str]) -> str:
        """
        Makes POST request containing data necessary for VK API
        :param method_name: string of VK API method
        :param parameters: dictionary of parameters and it's values, access token and version already included
        :return: json response from VK API or error, usually that happens because of the length of text in post
        """
        response = ''
        try:
            response = requests.post(self.get_url(method_name, self.combine_params(parameters))).json()
        except:
            response = f'ERROR: {requests.post(self.get_url(method_name, self.combine_params(parameters)))}'
        finally:
            return response
