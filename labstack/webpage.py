import requests


class WebpageService():
    def __init__(self, client):
        self.client = client
        self.url = 'https://webpage.labstack.com/api/v1'

    def image(self, request):
        return self.client._request('GET', '{}/image'
                                    .format(self.url), params=request)

    def pdf(self, request):
        return self.client._request('GET', '{}/pdf'
                                    .format(self.url), params=request)
