import requests


class CurrencyService():
    def __init__(self, client):
        self.client = client
        self.url = 'https://currency.labstack.com/api/v1'

    def convert(self, request):
        return self.client._request('GET', '{}/convert/{}/{}/{}'.
                                    format(self.url, request['amount'],
                                           request['from'], request['to']))

    def list(self, request):
        return self.client._request('GET', '{}/list'.format(self.url))
