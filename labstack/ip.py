import requests


class IPService():
    def __init__(self, client):
        self.client = client
        self.url = 'https://ip.labstack.com/api/v1'

    def lookup(self, request):
        return self.client._request('GET', '{}/{}'.format(self.url, request['ip']))
