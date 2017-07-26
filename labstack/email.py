import os
import base64
import requests
import json
from .common import API_URL

class _Email():
  def __init__(self, interceptor):
    self.path = '/email'
    self.interceptor = interceptor 
    
  def send(self, message):
    message._add_inlines()
    message._add_attachments()
    r = requests.post(API_URL + self.path, auth=self.interceptor, data=message.to_json())
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise EmailError(data['code'], data['message'])
    return EmailMessage.from_json(data) 

class EmailMessage():
  def __init__(self, to, from_, subject):
    self._inlines = []
    self._attachments = []
    self.to = to
    self.from_ = from_
    self.subject = subject
    self.body = ''
    self.inlines = []
    self.attachments = []
    self.status = ''

  def _add_inlines(self):
    for inline in self.inlines:
      with open(inline, 'rb') as file:
        self._inlines.append({
          'name': os.path.basename(inline),
          'content': base64.b64encode(file.read()).decode('utf-8')
        })
  
  def _add_attachments(self):
    for attachment in self.attachments:
      with open(attachment, 'rb') as file:
        self._attachments.append({
          'name': os.path.basename(attachment),
          'content': base64.b64encode(file.read()).decode('utf-8')
        })

  def add_inline(self, path):
    self.inlines.append(path)

  def add_attachment(self, path):
    self.attachments.append(path)

  def to_json(self):
    return json.dumps({
      'to': self.to,
      'from': self.from_,
      'subject': self.subject,
      'body': self.body,
      'inlines': self._inlines,
      'attachments': self._attachments
    })

  @classmethod
  def from_json(self, message):
    em = EmailMessage(message['to'], message['from'], message['subject'])
    em.id = message['id']
    em.time = message['time']
    em.status = message['status']
    return em
    
class EmailError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message
  
  def __str__(self):
    return self.message
  