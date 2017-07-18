import os
import base64
import json
import time
import threading
import asyncio
import requests
import arrow
from .common import API_URL

LevelDebug = 0
LevelInfo = 1
LevelWarn = 2
LevelError = 3
LevelFatal = 4
LevelOff = 5

levels = {
	LevelDebug: "DEBUG",
	LevelInfo:  "INFO",
	LevelWarn:  "WARN",
	LevelError: "ERROR",
	LevelFatal: "FATAL",
}

class _Log():
  def __init__(self, interceptor):
    self.path = '/log'
    self.interceptor = interceptor
    self._loop = None
    self.entries = []
    self.app_id = ''
    self.app_name = '' 
    self.tags = []
    self.level = LevelInfo
    self.batch_size = 60
    self.dispatch_interval = 60

  async def _schedule(self):
    await self._dispatch()
    await asyncio.sleep(self.dispatch_interval)
  
  async def _dispatch(self):
    if len(self.entries) == 0:
      return

    r = requests.post(API_URL + self.path, auth=self.interceptor, data=json.dumps(self.entries))
    if not 200 <= r.status_code < 300:
      data = r.json()
      raise LogError(data['code'], data['message'])

  def debug(self, format, *argv):
    self._log(LevelDebug, format, *argv)

  def info(self, format, *argv):
    self._log(LevelInfo, format, *argv)
    
  def warn(self, format, *argv):
    self._log(LevelWarn, format, *argv)
  
  def error(self, format, *argv):
    self._log(LevelError, format, *argv)
    
  def fatal(self, format, *argv):
    self._log(LevelFatal, format, *argv)

  def _log(self, level, format, *argv):
    if level < self.level:
      return

    if self._loop is None:
      self._loop = asyncio.new_event_loop()
      asyncio.set_event_loop(self._loop)
      self._loop.create_task(self._schedule())
      threading.Thread(target=self._loop.run_forever).start()
    
    message = format.format(*argv)
    self.entries.append({
      'time': arrow.now().format('YYYY-MM-DDTHH:mm:ss.SSSZ'),
		  'app_id': self.app_id,
		  'app_name': self.app_name,
		  'tags': self.tags,
		  'level': levels[self.level],
		  'message': message,
    })

    if len(self.entries) >= self.batch_size:
      try:
        self._dispatch()
      except LogError as err:
        print(err)
    
class LogError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message

  def __str__(self):
    return 'log error, code={0}, message={1}'.format(self.code, self.message)
  