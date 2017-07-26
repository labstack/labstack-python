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
    self.app_id = ''
    self.app_name = '' 
    self.level = Level.INFO
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

  def debug(self, fields):
    self._log(Level.DEBUG, fields)

  def info(self, fields):
    self._log(Level.INFO, fields)
    
  def warn(self, fields):
    self._log(Level.WARN, fields)
  
  def error(self, fields):
    self._log(Level.ERROR, fields)
    
  def fatal(self, fields):
    self._log(Level.FATAL, fields)

  def _log(self, level, fields):
    if level < self.level:
      return

    if self._loop is None:
      self._loop = asyncio.new_event_loop()
      asyncio.set_event_loop(self._loop)
      self._loop.create_task(self._schedule())
      threading.Thread(target=self._loop.run_forever).start()
    
    fields['time'] = arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ')
    fields['app_id'] = self.app_id
    fields['app_name'] = self.app_name
    fields['level'] = level.name
    self.entries.append(fields)

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
