import requests

class Currency():
  def __init__(self, client):
    self.client = client 

  def convert(self, from_, to, amount):
    return self.client._request('GET', '/currency/convert', params={
      'from': from_,
      'to': to,
      'amount': amount
    })

  def rates(self, base):
    return self.client._request('GET', '/currency/rates', params={'base': base})
