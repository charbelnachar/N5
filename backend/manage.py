#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from app.settings.base import get_config


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.base')
    """Run administrative tasks."""

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    host = get_config('HOST', default='127.0.0.1')
    port = get_config('PORT', default='8000')
    debug = get_config('DEBUG', default=False, cast=bool)

    if len(sys.argv) > 1 and sys.argv[1] == 'runserver':
        if debug:
            execute_from_command_line([sys.argv[0], 'runserver', f'{host}:{port}'])
        else:
            execute_from_command_line([sys.argv[0], 'runserver', f'{host}:{port}', '--noreload'])
    else:
        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
