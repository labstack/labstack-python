<a href="https://labstack.com"><img height="80" src="https://cdn.labstack.com/images/labstack-logo.svg"></a>

## Python Client

## Installation

`pip install labstack`

## Quick Start

[Sign up](https://labstack.com/signup) to get an API key

Create a file `app.py` with the following content:

```python
from labstack import Client, APIError

client = Client('<ACCOUNT_ID>', '<API_KEY>')

try:
  response = client.barcode_generate(format='qr_code', content='https://labstack.com')
  client.download(response['id'], '/tmp/' + response['name'])
except APIError as error:
  print(error)
```

From terminal run your app:

```sh
python app.py
```

## [API](https://labstack.com/api) | [Forum](https://forum.labstack.com)