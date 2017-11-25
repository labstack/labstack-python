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

  def barcode_generate(self, format=None, content=None, size=None):
    json = {
      'format': format,
      'content': content,
      'size': size
    }
    r = requests.post(API_URL + '/barcode/generate', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data
  
  def barcode_scan(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/barcode/scan', auth=self.interceptor, files=files)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data
  
  def dns_lookup(self, domain=None, type=None):
    json = {
      'domain': domain,
      'type': type
    }
    r = requests.post(API_URL + '/dns/lookup', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data

  def email_verify(self, email=None):
    json = {'email': email}
    r = requests.post(API_URL + '/email/verify', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data

  def image_compress(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/image/compress', auth=self.interceptor, files=files)
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
  
  def pdf_image(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/pdf/image', auth=self.interceptor, files=files)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data
  
  def text_sentiment(self, text=None):
    json = {'text': text}
    r = requests.post(API_URL + '/text/sentiment', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data
  
  def text_spell_check(self, text=None):
    json = {'text': text}
    r = requests.post(API_URL + '/text/spell-check', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data
  
  def text_summary(self, text=None, url=None, language=None, length=None):
    json = {
      'text': text,
      'url': url,
      'language': language,
      'length': length
    }
    r = requests.post(API_URL + '/text/summary', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data
  
  def webpage_pdf(self, url=None, size=None, layout=None):
    json = {
      'url': url,
      'size': size,
      'layout': layout
    }
    r = requests.post(API_URL + '/webpage/pdf', auth=self.interceptor,
      json=json)
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise APIError(data['code'], data['message'])
    return data

  def word_lookup(self, word=None):
    json = {'word': word}
    r = requests.post(API_URL + '/word/lookup', auth=self.interceptor,
      json=json)
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