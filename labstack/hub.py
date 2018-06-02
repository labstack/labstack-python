import time
import paho.mqtt.client as mqtt

class Hub():
  def __init__(self, account_id, api_key, device_id=None, message_handler=None):
    self.account_id = account_id
    self.client = mqtt.Client(client_id=device_id, clean_session=True)
    self.client.username_pw_set(account_id, api_key)
    # self.client.tls_set(ca_certs='labstack.com/cert.pem')
    self.handlers = {}
    def handler(client, userdata, msg):
      topic = self._denormalize_topic(msg.topic)
      if message_handler:
        message_handler(topic, msg.payload)
      h = self.handlers.get(topic)
      if h:
        h(topic, msg.payload)
    self.client.on_message = handler

  def _normalize_topic(self, topic):
    return '{}/{}'.format(self.account_id, topic)
  
  def _denormalize_topic(self, topic):
    return topic.lstrip(self.account_id + '/')
  
  def connect(self, handler=None):
    self.client.connect("hub.labstack.com", 1883)
    self.client.loop_start()
    def on_connect(client, userdata, flags, rc):
      if handler:
        handler()
    self.client.on_connect = on_connect

  def publish(self, topic, message):
    self.client.publish(self._normalize_topic(topic), message)

  # def subscribe(self, topic, handler, shared=False):
  def subscribe(self, topic, handler=None):
    # if shared:
    #   topic = '$queue/' + topic
    self.client.subscribe(self._normalize_topic(topic))
    self.handlers[topic] = handler

  def unsubscribe(self, topic):
    self.client.unsubscribe(self._normalize_topic(topic))

  def disconnect(self):
    self.client.loop_stop()
    self.client.disconnect()

  def run(self):
    try:
      while True:
        time.sleep(1)
    except (KeyboardInterrupt):
      pass