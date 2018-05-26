from django.conf import settings
from .cube import Cube
from .util import strip_port

def cube(get_response):
    options = settings.CUBE 
    c = Cube(**options)

    def middleware(request):
        r = c.start({
            'id': request.META.get('HTTP_X_REQUEST_ID'),
            'host': strip_port(request.get_host()),
            'path': request.path,
            'method': request.method,
            'bytes_in': int(request.META.get('CONTENT_LENGTH') or 0),
            # TODO: revisit
            'remote_ip': request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR'),
            'client_id': request.META.get('HTTP_X_CLIENT_ID'),
            'user_agent': request.META.get('HTTP_USER_AGENT')
        })

        response = get_response(request)

        # https://docs.djangoproject.com/en/2.0/_modules/django/middleware/common/#CommonMiddleware
        if not response.streaming and not response.has_header('Content-Length'):
            response['Content-Length'] = str(len(response.content))

        r['id'] = r['id'] or response.get('X-Request-ID')
        r['status'] = response.status_code
        r['bytes_out'] = int(response.get('Content-Length') or 0) 
        c.stop(r)

        return response

    return middleware