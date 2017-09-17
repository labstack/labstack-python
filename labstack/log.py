import os
import sys
import base64
import json
import time
import threading
import traceback
from enum import IntEnum
import requests
import arrow
from .common import API_URL

class _Log():
  def __init__(self, interceptor):
    self.path = '/log'
    self.interceptor = interceptor
    self.level = Level.INFO
    self.fields = {}

    # Automatically report uncaught fatal error
    def excepthook(type, value, trace):
      self.fatal(message=str(value), stack_trace=''.join(traceback.format_tb(trace)))
      sys.__excepthook__(type, value, trace)
    sys.excepthook = excepthook

  def _dispatch(self, entry):
    r = requests.post(API_URL + self.path, auth=self.interceptor, data=json.dumps(entry))
    if not 200 <= r.status_code < 300:
      data = r.json()
      raise LogError(data['code'], data['message'])

  def add_fields(self, **kwargs):
    self.fields.update(kwargs)

  def debug(self, **kwargs):
    self._log(Level.DEBUG, **kwargs)

  def info(self, **kwargs):
    self._log(Level.INFO, **kwargs)
    
  def warn(self, **kwargs):
    self._log(Level.WARN, **kwargs)
  
  def error(self, **kwargs):
    self._log(Level.ERROR, **kwargs)
    
  def fatal(self, **kwargs):
    self._log(Level.FATAL, **kwargs)

  def _log(self, level, **kwargs):
    if level < self.level:
      return
    
    kwargs['time'] = arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ')
    kwargs['level'] = level.name

    try:
      self._dispatch(kwargs)
    except LogError as err:
      print('log error: code={}, message={}'.format(err.code, err.message))

class Level(IntEnum):
  DEBUG = 0
  INFO = 1
  WARN = 2
  ERROR = 3
  FATAL = 4
  OFF = 5
    
class LogError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message

  def __str__(self):
    return self.message
