import requests

API_URL = 'https://api.labstack.com'

class _Interceptor(requests.auth.AuthBase):
  def __init__(self, api_key):
    self.api_key = api_key

  def __call__(self, r):
    r.headers['Authorization'] = 'Bearer ' + self.api_key
    return r

class Client():
  def __init__(self, account_id, api_key):
    self.api_key = api_key
    self.interceptor = _Interceptor(api_key)

  def _error(self, r):
    return not 200 <= r.status_code < 300

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
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def barcode_scan(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/barcode/scan', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def currency_convert(self, base=None):
    json = {'base': base}
    r = requests.post(API_URL + '/currency/convert', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
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
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def email_verify(self, email=None):
    json = {'email': email}
    r = requests.post(API_URL + '/email/verify', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def geocode_address(self, location=None, longitude=None, latitude=None, osm_tag=None, limit=None):
    json = {
      'location': location,
      'longitude': longitude,
      'latitude': latitude,
      'osm_tag': osm_tag,
      'limit': limit
    }
    r = requests.post(API_URL + '/geocode/address', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def geocode_ip(self, ip=None):
    json = {'ip': ip}
    r = requests.post(API_URL + '/geocode/ip', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def geocode_reverse(self, longitude=None, latitude=None, limit=None):
    json = {
      'longitude': longitude,
      'latitude': latitude,
      'limit': limit
    }
    r = requests.post(API_URL + '/geocode/reverse', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def image_compress(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/image/compress', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def image_resize(self, file=None, width=None, height=None, format=None):
    files = {'file': open(file, 'rb')}
    data = {
      'width': width,
      'height': height,
      'format': format
    }
    r = requests.post('{}/image/resize'.format(API_URL), auth=self.interceptor, 
      files=files, data=data)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def image_watermark(self, file=None, text=None, font=None, size=None, color=None, opacity=None,
    position=None, margin=None):
    files = {'file': open(file, 'rb')}
    data = {
      'text': text, 
      'font': font,
      'size': size,
      'color': color,
      'opacity': opacity,
      'position': position,
      'margin': margin
    }
    r = requests.post('{}/image/watermark'.format(API_URL), auth=self.interceptor, 
      files=files, data=data)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data  

  def pdf_compress(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/pdf/compress', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def pdf_image(self, file=None, extract=None):
    files = {'file': open(file, 'rb')}
    data = {
      'extract': extract
    }
    r = requests.post(API_URL + '/pdf/image', auth=self.interceptor, files=files, data=data)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def pdf_split(self, file=None, pages=None):
    files = {'file': open(file, 'rb')}
    data = {
      'pages': pages 
    }
    r = requests.post(API_URL + '/pdf/split', auth=self.interceptor, files=files, data=data)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def text_sentiment(self, text=None):
    json = {'text': text}
    r = requests.post(API_URL + '/text/sentiment', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def text_spellcheck(self, text=None):
    json = {'text': text}
    r = requests.post(API_URL + '/text/spellcheck', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
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
    if self._error(r):
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
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def word_lookup(self, word=None):
    json = {'word': word}
    r = requests.post(API_URL + '/word/lookup', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

class APIError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message
  
  def __str__(self):
    return self.messag