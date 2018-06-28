import time
import  requests
import paho.mqtt.client as mqtt

class Axis():
  def __init__(self, api_key, client_id, message_handler=None):
    self.api_key = api_key
    self.client_id = client_id
    self.message_handler = message_handler
    self.handlers = {}

  def _normalize_device_id(self, id):
    return '{}:{}'.format(self.project_id, id)

  def _normalize_topic(self, name):
    return '{}/{}'.format(self.project_id, name)
  
  def _denormalize_topic(self, name):
    return name.lstrip(self.project_id + '/')

  def _find_project_id(self):
    headers = {
      'Authorization': 'Bearer ' + self.api_key
    }
    r = requests.get('https://api.labstack.com/axis/key', headers=headers)
    if not 200 <= r.status_code < 300:
      pass
      # raise APIError(data['code'], data['message']) 
    data = r.json()
    self.project_id = data['project_id']
  
  def connect(self, handler=None):
    # Find project id
    self._find_project_id()

    # Connect
    self.client = mqtt.Client(client_id=self._normalize_device_id(self.client_id),
                              clean_session=True)
    self.client.username_pw_set(self.project_id, self.api_key)
    # self.client.tls_set(ca_certs='labstack.com/cert.pem')
    def message_handler(client, userdata, msg):
      topic = self._denormalize_topic(msg.topic)
      if self.message_handler:
        self.message_handler(topic, msg.payload)
      h = self.handlers.get(topic)
      if h:
        h(topic, msg.payload)
    self.client.on_message = message_handler
    self.client.connect("axis.labstack.com", 1883)
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