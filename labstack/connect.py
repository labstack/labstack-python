import paho.mqtt.client as mqtt

class _Connect():
  def __init__(self, account_id, api_key, client_id):
    self.account_id = account_id
    self.client = mqtt.Client(client_id=client_id, clean_session=True)
    self.client.username_pw_set(account_id, api_key)
    self.client.connect("iot.labstack.com", 1883)

  def on_connect(self, handler):
    self.client.on_connect = handler

  def on_message(self, handler):
    self.client.on_message = handler

  def publish(self, topic, message):
    self.client.publish('{}/{}'.format(self.account_id, topic), message)

  def subscribe(self, topic):
    self.client.subscribe('{}/{}'.format(self.account_id, topic))

  def disconnect(self):
    self.client.disconnect()

  def loop_forever(self):
    self.client.loop_forever()