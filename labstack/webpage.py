import requests

class Webpage():
  def __init__(self, client):
    self.client = client 
  
  def webpage(self, url, format=None, layout=None):
    return self.client._request('POST', '/webpage/pdf', params={
      'url': url,
      'format': format,
      'layout': layout
    })