import requests


class VKRequest:
    def __init__(self):
        with open('..\Information\\access_token.txt') as token:
            self.access_token = token.read()
        self.version = '5.74'

    def get_url(self, method_name, parameters):
        """
        Includes method and parameters in the URL
        :param method_name: string of VK API method
        :param parameters: dictionary of parameters and it's values, access token and version already included
        :return: string with correct for VK API URL
        """
        return f'https://api.vk.com/method/{method_name}?{parameters}&access_token={self.access_token}&v={self.version}'

    @staticmethod
    def combine_params(parameters):
        """
        Connects parameters to an ampersand to send a request
        :param parameters: dictionary of parameters and it's values from VK API method to join, access token and
        version already included
        :return: string with ampersand-connected parameters
        """
        return '&'.join([f'{key}={parameters[key]}' for key in parameters])

    def get(self, method_name, parameters):
        """
        Makes GET request containing data necessary for VK API
        :param method_name: string of VK API method
        :param parameters: dictionary of parameters and it's values, access token and version already included
        :return: json response from VK API
        """
        response = ''
        try:
            response = requests.get(self.get_url(method_name, self.combine_params(parameters))).json()
        except:
            response = 'ERROR'
        finally:
            return response

    def post(self, method_name, parameters):
        """
        Makes POST request containing data necessary for VK API
        :param method_name: string of VK API method
        :param parameters: dictionary of parameters and it's values, access token and version already included
        :return: json response from VK API
        """
        response = ''
        try:
            response = requests.post(self.get_url(method_name, self.combine_params(parameters))).json()
        except:
            response = 'ERROR'
        finally:
            return response
