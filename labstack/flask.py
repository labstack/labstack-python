from flask import request, g
from .cube import Cube
from .util import strip_port

def cube(app, api_key, **kwargs):
    c = Cube(api_key, **kwargs)
    
    @app.before_request
    def before_request():
        g._r = c.start({
            'id': request.headers.get('X-Request-ID'),
            'host': strip_port(request.host),
            'path': request.path,
            'method': request.method,
            'bytes_in': int(request.headers.get('Content-Length') or 0),
            # TODO: revisit
            'remote_ip': request.headers.get('X-Forwarded-For', request.remote_addr),
            'client_id': request.headers.get('X-Client-ID'),
            'user_agent': request.headers.get('User-Agent')
        })

    @app.after_request
    def after_request(response):
        r = g._r
        r['id'] = r['id'] or response.headers.get('X-Request-ID')
        r['status'] = response.status_code
        r['bytes_out'] = int(response.headers.get('Content-Length') or 0)
        c.stop(r)
        return response
