import signal
import time
import paho.mqtt.client as mqtt

class Hub():
  def __init__(self, account_id, api_key, client_id=None):
    self.account_id = account_id
    self.client = mqtt.Client(client_id=client_id, clean_session=True)
    self.client.username_pw_set(account_id, api_key)
    # self.client.tls_set(ca_certs='labstack.com/cert.pem')
    self.handlers = {}
    def handler(client, userdata, msg):
      self.handlers[msg.topic](msg.payload)
    self.client.on_message = handler
    self._run = True
    signal.signal(signal.SIGINT, self._stop)
    signal.signal(signal.SIGTERM, self._stop)
  
  def connect(self, handler=None):
    self.client.connect("hub.labstack.com", 1883)
    self.client.loop_start()
    def on_connect(client, userdata, flags, rc):
      handler()
    self.client.on_connect = on_connect 

  def publish(self, topic, message):
    self.client.publish('{}/{}'.format(self.account_id, topic), message)

  # def subscribe(self, topic, handler, shared=False):
  def subscribe(self, topic, handler):
    topic = '{}/{}'.format(self.account_id, topic)
    # if shared:
    #   topic = '$queue/' + topic
    self.client.subscribe(topic)
    self.handlers[topic] = handler

  def unsubscribe(self, topic):
    self.client.unsubscribe(topic)

  def disconnect(self):
    self.client.loop_stop()
    self.client.disconnect()

  def run(self):
    while self._run:
      time.sleep(1)

  def _stop(self, signum, frame):
    self._run = False
    self.disconnect()