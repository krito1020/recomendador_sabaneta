# WSGI para producción
import os
from django.core.wsgi import get_wsgi_application

# Asegúrate que este nombre coincida con tu archivo settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()