import requests


class EmailService():
    def __init__(self, client):
        self.client = client
        self.url = 'https://email.labstack.com/api/v1'

    def verify(self, request):
        return self.client._request('GET', '{}/verify/{}'.
                                    format(self.url, request['email']))
