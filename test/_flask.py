import os
from flask import Flask
from labstack.flask import cube

app = Flask(__name__)

# Cube
cube(app, os.getenv('LABSTACK_KEY'), batch_size=1)

@app.route("/")
def hello():
    return "Hello, World!"
