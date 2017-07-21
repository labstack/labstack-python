import os
import requests
import json
from .common import API_URL

class _Store():
  def __init__(self, interceptor):
    self.path = '/store'
    self.interceptor = interceptor 
    
  def insert(self, key, value):
    entry = StoreEntry(key, value)
    r = requests.post(API_URL + self.path, auth=self.interceptor, data=entry.to_json())
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise StoreError(data['code'], data['message'])
    return StoreEntry.from_json(data) 

  def get(self, key):
    r = requests.get(API_URL + self.path + '/' + key, auth=self.interceptor)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise StoreError(data['code'], data['message'])
    return StoreEntry.from_json(data) 

  def query(self, filters='', limit=None, offset=None):
    params = {
      'filters': filters,
      'limit': limit,
      'offset': offset
    }
    r = requests.get(API_URL + self.path, auth=self.interceptor, params=params)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise StoreError(data['code'], data['message'])
    return StoreQueryResponse.from_json(data) 

  def update(self, key, value):
    entry = StoreEntry(key, value)
    r = requests.put(API_URL + self.path + '/' + key, auth=self.interceptor, data=entry.to_json())
    if not 200 <= r.status_code < 300:
      data = r.json()
      raise StoreError(data['code'], data['message'])

  def delete(self, key):
    r = requests.delete(API_URL + self.path + '/' + key, auth=self.interceptor)
    if not 200 <= r.status_code < 300:
      data = r.json()
      raise StoreError(data['code'], data['message'])

class StoreEntry():
  def __init__(self, key=None, value=None):
    self.key = key
    self.value = value
    self.created_at = None
    self.updated_at = None

  def to_json(self):
    return json.dumps({
      'key': self.key,
      'value': self.value
    })

  @classmethod
  def from_json(self, entry):
    se = StoreEntry(entry['key'], entry['value'])
    se.created_at = entry['created_at']
    se.updated_at = entry['updated_at']
    return se

class StoreQueryResponse():
  def __init__(self):
    self.total = 0
    self.entries = []

  @classmethod
  def from_json(self, response):
    qr = StoreQueryResponse()
    qr.total = response['total']
    qr.entries = response['entries']
    return qr

class StoreError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message

  def __str__(self):
    return 'store error, code={0}, message={1}'.format(self.code, self.message)
  