import requests

class Post():
  def __init__(self, client):
    self.client = client 
  
  def verify(self, email):
    return self.client._request('GET', '/post/verify', params={'email': email})