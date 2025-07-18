#!/usr/bin/env python
import os
import sys
from pathlib import Path

if __name__ == "__main__":
    # Asegura que Python encuentra el módulo de configuración settings.py
    BASE_DIR = Path(__file__).resolve().parent
    sys.path.append(str(BASE_DIR))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)