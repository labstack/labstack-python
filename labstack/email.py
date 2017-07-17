import os
import base64
import requests
import json
from .common import API_URL

def _email_file_from_path(path):
  with open(path, 'rb') as file:
    return {
      'name': os.path.basename(path),
      'content': base64.b64encode(file.read()).decode('utf-8')
    }

class _Email():
  def __init__(self, interceptor):
    self.path = '/email'
    self.interceptor = interceptor 
    
  def send(self, message):
    message._add_files()
    r = requests.post(API_URL + self.path, auth=self.interceptor, data=message.to_json())
    data = r.json()
    if not 200 <= r.status_code < 300:
      raise EmailError(data['code'], data['message'])
    return EmailMessage.from_json(data) 

class EmailMessage():
  def __init__(self, to, sender, subject):
    self._inlines = []
    self._attachments = []
    self.to = to
    self.sender = sender 
    self.subject = subject
    self.body = ''
    self.inlines = []
    self.attachments = []
    self.status = ''

  def _add_files(self):
    for path in self.inlines:
      self._inlines.append(_email_file_from_path(path))
    for path in self.attachments:
      self._attachments.append(_email_file_from_path(path))

  def add_inline(self, path):
    self.inlines.append(path)

  def add_attachment(self, path):
    self.attachments.append(path)

  def to_json(self):
    return json.dumps({
      'to': self.to,
      'from': self.sender,
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
    return 'email error, code={0}, message={1}'.format(self.code, self.message)
  