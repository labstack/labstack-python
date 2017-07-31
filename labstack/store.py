import os
import requests
import json
from .common import API_URL

class _Store():
  def __init__(self, interceptor):
    self.path = '/store'
    self.interceptor = interceptor 
    
  def insert(self, collection, document):
    r = requests.post('{}{}/{}'.format(API_URL, self.path, collection), auth=self.interceptor, json=document)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise StoreError(data['code'], data['message'])
    return data

  def get(self, collection, id):
    r = requests.get('{}{}/{}/{}'.format(API_URL, self.path, collection, id), auth=self.interceptor)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise StoreError(data['code'], data['message'])
    return data

  def search(self,
             collection,
             query=None,
             query_string='*',
             sort=None,
             size=None,
             from_=None):
    params = {
      'query': query,
      'query_string': query_string,
      'sort': sort,
      'size': size,
      'from': from_ 
    }
    r = requests.post('{}{}/{}/search'.format(API_URL, self.path, collection), auth=self.interceptor, json=params)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise StoreError(data['code'], data['message'])
    return data

  def update(self, collection, id, document):
    r = requests.patch('{}{}/{}/{}'.format(API_URL, self.path, collection, id), auth=self.interceptor, json=document)
    if not 200 <= r.status_code < 300:
      data = r.json()
      raise StoreError(data['code'], data['message'])

  def delete(self, collection, id):
    r = requests.delete('{}{}/{}/{}'.format(API_URL, self.path, collection, id), auth=self.interceptor)
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

# class StoreSearchResponse():
#   def __init__(self):
#     self.total = 0
#     self.documents = []

#   @classmethod
#   def from_json(self, response):
#     qr = StoreSearchResponse()
#     qr.total = response['total']
#     for entry in response['entries']:
#       qr.documents.append(StoreEntry.from_json(entry))
#     return qr

class StoreError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message

  def __str__(self):
    return self.message
  