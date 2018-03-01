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

  def currency_convert(self, from=None, to=None, value=None):
    params = {
      'from': from,
      'to': to,
      'value': value
    }
    r = requests.get(API_URL + '/currency/convert', auth=self.interceptor,
      params=params)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def currency_rates(self, base=None):
        params = {'base': base}
    r = requests.get(API_URL + '/currency/rates', auth=self.interceptor,
      params=params)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def email_verify(self, email=None):
    params = {'email': email}
    r = requests.get(API_URL + '/email/verify', auth=self.interceptor,
      params=params)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def geocode_address(self, location=None, longitude=None, latitude=None, osm_tag=None, limit=None):
    params = {
      'location': location,
      'longitude': longitude,
      'latitude': latitude,
      'osm_tag': osm_tag,
      'limit': limit
    }
    r = requests.get(API_URL + '/geocode/address', auth=self.interceptor,
      params=params)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def geocode_ip(self, ip=None):
    params = {'ip': ip}
    r = requests.get(API_URL + '/geocode/ip', auth=self.interceptor,
      params=params)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def geocode_reverse(self, longitude=None, latitude=None, limit=None):
    params = {
      'longitude': longitude,
      'latitude': latitude,
      'limit': limit
    }
    r = requests.get(API_URL + '/geocode/reverse', auth=self.interceptor,
      params=params)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def compress_audio(self, file=None):
        files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/compress/audio', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def compress_image(self, file=None):
    files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/compress/image', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def compress_pdf(self, file=None):
        files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/compress/pdf', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def compress_video(self, file=None):
        files = {'file': open(file, 'rb')}
    r = requests.post(API_URL + '/compress/video', auth=self.interceptor, files=files)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def watermark_image(self, file=None, text=None, font=None, size=None, color=None, opacity=None,
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
    r = requests.post('{}/watermark/image'.format(API_URL), auth=self.interceptor, 
      files=files, data=data)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data  
  
  def nlp_sentiment(self, text=None):
    json = {'text': text}
    r = requests.post(API_URL + '/text/sentiment', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def nlp_spellcheck(self, text=None):
    json = {'text': text}
    r = requests.post(API_URL + '/text/spellcheck', auth=self.interceptor,
      json=json)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data
  
  def nlp_summary(self, text=None, url=None, language=None, length=None):
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
  
  def webpage_pdf(self, url=None, layout=None, format=None):
    params = {
      'url': url,
      'layout': layout
      'format': format,
    }
    r = requests.get(API_URL + '/webpage/pdf', auth=self.interceptor,
      params=params)
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