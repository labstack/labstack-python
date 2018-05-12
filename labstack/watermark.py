import requests

class Watermark():
  def __init__(self, client):
    self.client = client 
  
  def image(self, file, text, font=None, size=None, color=None, opacity=None,
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
    return self.client._request('POST', '/watermark/image', files=files, data=data)