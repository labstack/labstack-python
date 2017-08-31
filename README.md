<a href="https://labstack.com"><img height="80" src="https://cdn.labstack.com/images/labstack-logo.svg"></a>

## Python Client

## Installation

`pip install labstack`

## Quick Start

[Sign up](https://labstack.com/signup) to get an API key

Create a file `app.py` with the following content:

```python
from labstack import Client

client = Client('<ACCOUNT_ID>', '<API_KEY>')
store = client.store()
doc = store.insert('users', {
  name: 'Jack',
  location: 'Disney'
})
print(doc)
```

From terminal run your app:

```sh
python app.py
```

## [Docs](https://labstack.com/docs) | [Forum](https://forum.labstack.com)