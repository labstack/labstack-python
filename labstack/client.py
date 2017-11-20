import requests

API_URL = 'https://api.labstack.com'

class _Interceptor(requests.auth.AuthBase):
  def __init__(self, api_key):
    self.api_key = api_key

  def __call__(self, r):
    r.headers['Authorization'] = 'Bearer ' + self.api_key
    return r

class Client():
  def __init__(self, api_key):
    self.api_key = api_key
    self.interceptor = _Interceptor(api_key)

  def download(self, id, path):
    r = requests.get('{}/download/{}'.format(API_URL, id), stream=True)
    with open(path, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024): 
        if chunk:
          f.write(chunk)
          f.flush()

  def barcode_generate(self, format=None, content=None):
    json = {
      'format': format,
      'content': content
    }
    r = requests.post('{}/barcode/generate'.format(API_URL), auth=self.interceptor, json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data

  def image_compress(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post('{}/image/compress'.format(API_URL), auth=self.interceptor, files=files)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data

  def image_resize(self, file=None, width=None, height=None, crop=None):
    files = {'file': open(file, 'rb')}
    data = {
      'width': width,
      'height': height,
      'crop': crop
    }
    r = requests.post('{}/image/resize'.format(API_URL), auth=self.interceptor, 
      files=files, data=data)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data  

class APIError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message
  
  def __str__(self):
    return self.messag