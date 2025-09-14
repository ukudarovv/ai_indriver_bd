#!/usr/bin/env python
"""
Скрипт для запуска Django сервера с автоматической настройкой
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_registry.settings')
    django.setup()
    
    # Выполняем миграции
    print("Выполняем миграции...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Запускаем сервер
    print("Запускаем сервер...")
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])
