import requests

class Currency():
  def __init__(self, client):
    self.client = client 

  def convert(self, amount, from_, to):
    return self.client._request('GET', '/currency/convert', params={
      'amount': amount,
      'from': from_,
      'to': to
    })

  def rates(self, base):
    return self.client._request('GET', '/currency/rates', params={'base': base})
