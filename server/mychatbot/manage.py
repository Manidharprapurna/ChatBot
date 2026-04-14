#!/usr/bin/env python
import os
import sys
from dotenv import load_dotenv

# FORCE LOAD .env FROM ROOT
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mychatbot.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()