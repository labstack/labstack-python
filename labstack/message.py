import paho.mqtt.client as mqtt

class _Message():
  def __init__(self, account_id, api_key, client_id):
    self.account_id = account_id
    self.client = mqtt.Client(client_id=client_id, clean_session=True)
    self.client.username_pw_set(account_id, api_key)
    self.client.connect("iot.labstack.com", 1883)

  def connect_handler(self, handler):
    def connect_handler(client, userdata, flags, rc):
      handler()
    self.client.on_connect = connect_handler

  def data_handler(self, handler):
    def data_handler(client, userdata, msg):
      handler(msg.topic, msg.payload)
    self.client.on_message = data_handler

  def publish(self, topic, message):
    self.client.publish('{}/{}'.format(self.account_id, topic), message)

  def subscribe(self, topic, shared=False):
    topic = '{}/{}'.format(self.account_id, topic)
    if shared:
      topic = '$queue/' + topic
    self.client.subscribe(topic)

  def disconnect(self):
    self.client.disconnect()

  def loop_forever(self):
    self.client.loop_forever()