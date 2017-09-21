import requests
from .hub import _Hub
from .jet import _Jet

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

  def hub(self, client_id):
    return _Hub(self.account_id, self.api_key, client_id)

  def jet(self):
    return _Jet(self.interceptor)
  