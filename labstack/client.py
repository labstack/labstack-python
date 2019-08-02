import requests
from .currency import CurrencyService
from .domain import DomainService
from .email import EmailService
from .ip import IPService
from .webpage import WebpageService


class _Interceptor(requests.auth.AuthBase):
    def __init__(self, key):
        self.key = key

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.key
        return r


class Client():
    def __init__(self, key):
        self.key = key
        self.interceptor = _Interceptor(key)

    def _request(self, method, url, params=None, files=None, data=None):
        r = requests.request(method, url, auth=self.interceptor,
                             params=params, files=files, data=data)
        data = r.json()
        if self._is_error(r):
            raise LabStackError(data['code'], data['message'])
        return data

    def _is_error(self, r):
        return not 200 <= r.status_code < 300

    def currency(self):
        return CurrencyService(self)

    def domain(self):
        return DomainService(self)

    def email(self):
        return EmailService(self)

    def ip(self):
        return IPService(self)

    def webpage(self):
        return WebpageService(self)


class LabStackError(Exception):
    def __init__(self, statusCode, code, message):
        self.statusCode = statusCode
        self.code = code
        self.message = message

    def __str__(self):
        return self.message
