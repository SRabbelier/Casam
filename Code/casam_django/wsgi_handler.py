import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'casam_django.settings'

import django.core.handlers.wsgi

_application = django.core.handlers.wsgi.WSGIHandler()

# cpbotha: make sure SSL is on (workaround might not be necessary)
def application(environ, start_response):
    if environ['wsgi.url_scheme'] == 'https':
        environ['HTTPS'] = 'on'
    return _application(environ, start_response)

