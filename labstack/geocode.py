import requests

class Geocode():
  def __init__(self, client):
    self.client = client 
  
  def address(self, location, longitude=None, latitude=None, osm_tag=None, limit=None):
    return self.client._request('GET', '/geocode/address', params={
      'location': location,
      'longitude': longitude,
      'latitude': latitude,
      'osm_tag': osm_tag,
      'limit': limit
    })
  
  def ip(self, ip):
    return self.client._request('GET', '/geocode/ip', params={'ip': ip})
  
  def reverse(self, longitude, latitude, limit=None):
    return self.client._request('GET', '/geocode/reverse', params={
      'longitude': longitude,
      'latitude': latitude,
      'limit': limit
    })
