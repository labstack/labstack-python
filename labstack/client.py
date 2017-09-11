import requests
from .message import _Message
from .email import _Email
from .log import _Log
from .store import _Store

class _Interceptor(requests.auth.AuthBase):
  def __init__(self, api_key):
    self.api_key = api_key

  def __call__(self, r):
    r.headers['Authorization'] = 'Bearer ' + self.api_key
    r.headers['Content-Type'] = 'application/json; charset=utf-8'
    return r

class Client():
  def __init__(self, account_id, api_key):
    self.account_id = account_id
    self.api_key = api_key
    self.interceptor = _Interceptor(api_key)

  def message(self, client_id):
    return _Message(self.account_id, self.api_key, client_id)

  def email(self):
    return _Email(self.interceptor)

  def log(self):
    log = _Log(self.interceptor)
    return log
  
  def store(self):
    return _Store(self.interceptor)
  