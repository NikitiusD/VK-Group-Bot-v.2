import requests


class VKRequest:
    def __init__(self):
        with open('..\Information\\access_token.txt') as token:
            self.access_token = token.read()
        self.version = '5.74'

    def get_url(self, method_name, parameters):
        return f'https://api.vk.com/method/{method_name}?{parameters}&access_token={self.access_token}&v={self.version}'

    @staticmethod
    def combine_params(parameters):
        params = ''
        for key in parameters:
            params += f'{key}={parameters[key]}&'
        return params

    def get(self, method_name, parameters):
        return requests.get(self.get_url(method_name, self.combine_params(parameters))).json()

    def post(self, method_name, parameters):
        return requests.post(self.get_url(method_name, self.combine_params(parameters))).json()


