<a href="https://labstack.com"><img height="80" src="https://cdn.labstack.com/images/labstack-logo.svg"></a>

## Python Client

## Installation

`pip install labstack`

## Quick Start

[Sign up](https://labstack.com/signup) to get an API key

Create a file `app.py` with the following content:

```python
from labstack import Client, JetMessage

client = Client('ACCOUNT_ID', '<API_KEY>')
jet = client.jet()
message = JetMessage('jack@labstack.com', 'LabStack', 'Hello')
message.body = 'hello'
message.add_inline('walle.png')
message = jet.send(message)
```

From terminal run your app:

```sh
python app.py
```

## [Documentation](https://labstack.com/docs) | [Forum](https://forum.labstack.com)