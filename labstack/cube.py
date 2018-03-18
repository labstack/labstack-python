import os
import time
import socket
import threading
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import psutil

sched = BackgroundScheduler()

class Cube():
    def __init__(self, api_key, node=socket.gethostname(), batch_size=60,
                dispatch_interval=60, tags=None):
        self.api_key = api_key
        self.node = node
        self.batch_size = batch_size
        self.dispatch_interval = dispatch_interval
        self.tags = tags
        self.uptime = 0
        self.cpu = 0.0
        self.memory = 0
        self.active_requests = 0
        self.requests = []
        self.lock = threading.Lock() 
        
        def system():
            p = psutil.Process(os.getpid())
            self.uptime = int(datetime.now().timestamp() - p.create_time())
            self.cpu = p.cpu_percent()
            self.memory = p.memory_full_info().rss

        sched.add_job(self._dispatch, 'interval', seconds=dispatch_interval)
        sched.add_job(system, 'interval', seconds=1)
        sched.start()

    def _dispatch(self):
        if not self.requests:
            return

        r = requests.post('https://api.labstack.com/cube', headers={
                'User-Agent': 'labstack/cube',
                'Authorization': 'Bearer ' + self.api_key
            }, json=self.requests)
        if not 200 <= r.status_code < 300:
            # TOTO: handler error
            print('cube error', r.json())
    
        # Reset requests
        self.requests.clear()

    def start(self, request):
        with self.lock:
            self.active_requests += 1

        request['time'] = int(datetime.now().timestamp() * 1000000)
        request['active'] = self.active_requests
        request['node'] = self.node
        request['uptime'] = self.uptime
        request['cpu'] = self.cpu
        request['memory'] = self.memory
        request['tags'] = self.tags
        self.requests.append(request)

        return request

    def stop(self, request):
        with self.lock:
            self.active_requests -= 1
        request['latency'] = int(datetime.now().timestamp() * 1000000) - request['time']

        # Dispatch batch
        if len(self.requests) >= self.batch_size:
            threading.Thread(target=self._dispatch).start()
            