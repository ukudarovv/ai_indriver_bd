#!/usr/bin/env python
"""
Скрипт для проверки данных в базе
"""
import os
import django

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_registry.settings')
    django.setup()
    
    from api.models import Accident, CarPart, Vehicle
    
    print("=== Проверка данных ===")
    
    # Проверяем количество аварий
    accidents_count = Accident.objects.count()
    print(f"Всего аварий: {accidents_count}")
    
    # Проверяем количество деталей
    parts_count = CarPart.objects.count()
    print(f"Всего деталей: {parts_count}")
    
    # Проверяем аварии с поврежденными деталями
    accidents_with_parts = Accident.objects.filter(damaged_parts__isnull=False).distinct().count()
    print(f"Аварий с поврежденными деталями: {accidents_with_parts}")
    
    # Показываем примеры аварий с деталями
    print("\n=== Примеры аварий с поврежденными деталями ===")
    for accident in Accident.objects.filter(damaged_parts__isnull=False).distinct()[:3]:
        print(f"\nАвария ID {accident.accident_id}:")
        print(f"  Дата: {accident.date}")
        print(f"  ТС: {accident.vehicle}")
        print(f"  Поврежденные детали:")
        for part in accident.damaged_parts.all():
            print(f"    - {part.name} ({part.category})")
    
    # Показываем все доступные детали
    print("\n=== Все доступные детали ===")
    for category in CarPart.objects.values_list('category', flat=True).distinct():
        print(f"\n{category}:")
        for part in CarPart.objects.filter(category=category):
            print(f"  - {part.name}")
