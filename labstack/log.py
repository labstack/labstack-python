import os
import base64
import json
import time
import threading
from enum import IntEnum
import asyncio
import requests
import arrow
from .common import API_URL

class _Log():
  def __init__(self, interceptor):
    self.path = '/log'
    self.interceptor = interceptor
    self._loop = None
    self.entries = []
    self.level = Level.INFO
    self.fields = {}
    self.batch_size = 60
    self.dispatch_interval = 60

  async def _schedule(self):
    while True:
      try:
        await self._dispatch()
      except LogError as err:
        print('log error: code={}, message={}'.format(err.code, err.message))
      await asyncio.sleep(self.dispatch_interval)
  
  async def _dispatch(self):
    if len(self.entries) == 0:
      return
    try:
      r = requests.post(API_URL + self.path, auth=self.interceptor, data=json.dumps(self.entries))
      if not 200 <= r.status_code < 300:
        data = r.json()
        raise LogError(data['code'], data['message'])
    finally:
      self.entries.clear()

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

    if self._loop is None:
      self._loop = asyncio.new_event_loop()
      asyncio.set_event_loop(self._loop)
      self._loop.create_task(self._schedule())
      threading.Thread(target=self._loop.run_forever).start()
    
    kwargs['time'] = arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ')
    for k, v in self.fields.items():
      kwargs[k]  = v
    kwargs['level'] = level.name
    self.entries.append(kwargs)

    if len(self.entries) >= self.batch_size:
      try:
        self._dispatch()
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
