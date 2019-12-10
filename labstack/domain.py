import requests


class DomainService():
    def __init__(self, client):
        self.client = client
        self.url = 'https://domain.labstack.com/api/v1'

    def dns(self, request):
        return self.client._request('GET', '{}/{}/{}'.
                                    format(self.url, request['type'], request['domain']))

    def search(self, request):
        return self.client._request('GET', '{}/search'.
                                    format(self.url, params={'q': request['q']}))

    def status(self, request):
        return self.client._request('GET', '{}/status/{}'.
                                    format(self.url, request['domain']))

    def whois(self, request):
        return self.client._request('GET', '{}/whois/{}'.
                                    format(self.url, request['domain']))
