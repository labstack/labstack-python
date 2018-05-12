import requests
from .currency import Currency
from .geocode import Geocode 
from .post import Post 
from .watermark import Watermark 
from .webpage import Webpage 

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

  def _request(self, method, path, params=None, files=None, data=None):
    r = requests.request(method, API_URL + path, auth=self.interceptor,
                          params=params, files=files, data=data)
    data = r.json()
    if self._error(r):
      raise APIError(data['code'], data['message'])
    return data

  def _error(self, r):
    return not 200 <= r.status_code < 300

  def currency(self):
    return Currency(self)

  def geocode(self):
    return Geocode(self)

  def post(self):
    return Post(self)
  
  def watermark(self):
    return Watermark(self)

  def webpage(self):
    return Webpage(self)

  def download(self, id, path):
    r = requests.get('{}/download/{}'.format(API_URL, id), stream=True)
    with open(path, 'wb') as f:
      for chunk in r.iter_content(chunk_size=1024): 
        if chunk:
          f.write(chunk)
          f.flush()
    
  # def compress_audio(self, file=None):
  #       files = {'file': open(file, 'rb')}
  #   r = requests.post(API_URL + '/compress/audio', auth=self.interceptor, files=files)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data

  # def compress_image(self, file=None):
  #   files = {'file': open(file, 'rb')}
  #   r = requests.post(API_URL + '/compress/image', auth=self.interceptor, files=files)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data
  
  # def compress_pdf(self, file=None):
  #       files = {'file': open(file, 'rb')}
  #   r = requests.post(API_URL + '/compress/pdf', auth=self.interceptor, files=files)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data
  
  # def compress_video(self, file=None):
  #       files = {'file': open(file, 'rb')}
  #   r = requests.post(API_URL + '/compress/video', auth=self.interceptor, files=files)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data

  # def nlp_sentiment(self, text=None):
  #   json = {'text': text}
  #   r = requests.post(API_URL + '/text/sentiment', auth=self.interceptor,
  #     json=json)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data
  
  # def nlp_spellcheck(self, text=None):
  #   json = {'text': text}
  #   r = requests.post(API_URL + '/text/spellcheck', auth=self.interceptor,
  #     json=json)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data
  
  # def nlp_summary(self, text=None, url=None, language=None, length=None):
  #   json = {
  #     'text': text,
  #     'url': url,
  #     'language': language,
  #     'length': length
  #   }
  #   r = requests.post(API_URL + '/text/summary', auth=self.interceptor,
  #     json=json)
  #   data = r.json()
  #   if self._error(r):
  #     raise APIError(data['code'], data['message'])
  #   return data
  
class APIError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message
  
  def __str__(self):
    return self.message