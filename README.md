<a href="https://labstack.com"><img height="80" src="https://cdn.labstack.com/images/labstack-logo.svg"></a>

## Python Client

## Installation

`pip install labstack`

## Quick Start

[Sign up](https://labstack.com/signup) to get an API key

Create a file `app.py` with the following content:

```python
from labstack import Client, APIError

client = new Client('<API_KEY>')
geocode = client.geocode()

try:
  response = geocode.address('eiffel tower')
  print(response)
except APIError as error:
  print(error)
```

From terminal run your app:

```sh
python app.py
```

## [Docs](https://labstack.com/docs/api) | [Forum](https://forum.labstack.com)
