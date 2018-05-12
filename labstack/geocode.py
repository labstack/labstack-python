import requests

class Geocode():
  def __init__(self, client):
    self.client = client 
  
  def address(self, location, latitude=None, longitude=None, osm_tag=None,
              format=None, limit=None):
    return self.client._request('GET', '/geocode/address', params={
      'location': location,
      'latitude': latitude,
      'longitude': longitude,
      'osm_tag': osm_tag,
      'format': format,
      'limit': limit
    })
  
  def ip(self, ip, format=None):
    return self.client._request('GET', '/geocode/ip', params={
      'ip': ip,
      'format': format
    })
  
  def reverse(self, latitude, longitude, limit=None):
    return self.client._request('GET', '/geocode/reverse', params={
      'latitude': latitude,
      'longitude': longitude,
      'format': format,
      'limit': limit
    })
