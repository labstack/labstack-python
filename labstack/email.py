import requests

class Email():
  def __init__(self, client):
    self.client = client 
  
  def verify(self, email):
    return self.client._request('GET', '/email/verify', params={'email': email})