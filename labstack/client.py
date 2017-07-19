import requests
from .email import _Email
from .log import _Log
from .store import _Store

class Client():
  def __init__(self, api_key):
    self.interceptor = _Interceptor(api_key)
    self.app_id = ''
    self.app_name = ''

  def email(self):
    return _Email(self.interceptor)

  def log(self):
    log = _Log(self.interceptor)
    log.app_id = self.app_id
    log.app_name = self.app_name
    return log
  
  def store(self):
    return _Store(self.interceptor)

class _Interceptor(requests.auth.AuthBase):
  def __init__(self, api_key):
    self.api_key = api_key

  def __call__(self, r):
    r.headers['Authorization'] = 'Bearer ' + self.api_key
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    return r