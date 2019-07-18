"""
WSGI config for reverse project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import sys
import os
import django

from django.core.wsgi import get_wsgi_application

sys.path.append("C:/Users/Narthil/Learning/django/reverse/reverse")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reverse.settings')
django.setup()

application = get_wsgi_application()
