#!/usr/bin/env python
import os
import sys
from . import *

# def main():
#     import puma
#     import pumagui
#     from django.core.management import call_command
#     from django.core.wsgi import get_wsgi_application
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puma.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     application = get_wsgi_application()
#     call_command('runserver', '127.0.0.1:8000')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'puma.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
