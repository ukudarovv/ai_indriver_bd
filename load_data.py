#!/usr/bin/env python
"""
Скрипт для загрузки тестовых данных в Django модели
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_registry.settings')
    django.setup()
    
    from api.models import Owner, DriverLicense, Vehicle, Plate, Insurer, InsurancePolicy, Accident
    from datetime import date, timedelta
    import random
    import string
    
    print("Создаем тестовые данные...")
    
    # Очищаем существующие данные
    Accident.objects.all().delete()
    InsurancePolicy.objects.all().delete()
    Plate.objects.all().delete()
    Vehicle.objects.all().delete()
    DriverLicense.objects.all().delete()
    Owner.objects.all().delete()
    Insurer.objects.all().delete()
    
    # Создаем страховые компании
    insurers = [
        Insurer.objects.create(name='Jusan Insurance'),
        Insurer.objects.create(name='Nomad Insurance'),
        Insurer.objects.create(name='Eurasia Insurance'),
    ]
    
    # Создаем владельцев и их данные
    owners = []
    for i in range(1, 101):  # Создаем 100 владельцев
        owner = Owner.objects.create(
            full_name=f'Владелец {i}',
            iin=f'{700000000000 + i:012d}',
            dob=date(1970, 1, 1) + timedelta(days=random.randint(0, 15000)),
            phone=f'+7701{random.randint(1000000, 9999999)}'
        )
        owners.append(owner)
        
        # Создаем водительское удостоверение
        DriverLicense.objects.create(
            owner=owner,
            number=f'DL-{i:07d}',
            categories=random.choice(['A', 'B', 'B,BE', 'C', 'D']),
            issued_at=date.today() - timedelta(days=365 * random.randint(1, 10)),
            expires_at=date.today() + timedelta(days=365 * random.randint(1, 5)),
            status='valid'
        )
    
    # Создаем транспортные средства
    vehicles = []
    makes_models = [
        ('Toyota', 'Camry'),
        ('VW', 'Golf'),
        ('Hyundai', 'Elantra'),
        ('Kia', 'Rio'),
        ('Lada', 'Vesta'),
        ('Nissan', 'Qashqai'),
    ]
    colors = ['white', 'black', 'silver', 'blue', 'red']
    
    for i, owner in enumerate(owners):
        make, model = random.choice(makes_models)
        vin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))
        
        vehicle = Vehicle.objects.create(
            owner=owner,
            vin=vin,
            make=make,
            model=model,
            year=2005 + random.randint(0, 20),
            color=random.choice(colors)
        )
        vehicles.append(vehicle)
        
        # Создаем номерной знак
        plate_number = f'{random.randint(100, 999)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}{random.randint(10, 99)}'
        Plate.objects.create(
            vehicle=vehicle,
            plate_number=plate_number,
            region=f'Region{random.randint(1, 17)}'
        )
        
        # Создаем страховой полис OSAGO
        InsurancePolicy.objects.create(
            vehicle=vehicle,
            insurer=random.choice(insurers),
            policy_number=f'OSG-{random.randint(1000000, 9999999)}',
            type='OSAGO',
            valid_from=date.today() - timedelta(days=random.randint(0, 60)),
            valid_to=date.today() + timedelta(days=random.randint(10, 300)),
            status='active' if random.random() < 0.85 else 'expired'
        )
        
        # Создаем страховой полис KASKO (не для всех)
        if random.random() < 0.3:
            InsurancePolicy.objects.create(
                vehicle=vehicle,
                insurer=random.choice(insurers),
                policy_number=f'KSK-{random.randint(1000000, 9999999)}',
                type='KASKO',
                valid_from=date.today() - timedelta(days=random.randint(0, 60)),
                valid_to=date.today() + timedelta(days=random.randint(100, 400)),
                status='active' if random.random() < 0.9 else 'expired'
            )
        
        # Создаем аварии (не для всех)
        if random.random() < 0.2:
            Accident.objects.create(
                vehicle=vehicle,
                date=date.today() - timedelta(days=random.randint(10, 800)),
                severity=random.choice(['minor', 'moderate', 'severe']),
                location=random.choice(['Алматы', 'Астана', 'Шымкент', 'Караганда']),
                description='Имитация ДТП',
                fault_party=random.choice(['owner', 'other', 'unknown'])
            )
    
    print(f"Создано:")
    print(f"- {Owner.objects.count()} владельцев")
    print(f"- {DriverLicense.objects.count()} водительских удостоверений")
    print(f"- {Vehicle.objects.count()} транспортных средств")
    print(f"- {Plate.objects.count()} номерных знаков")
    print(f"- {Insurer.objects.count()} страховых компаний")
    print(f"- {InsurancePolicy.objects.count()} страховых полисов")
    print(f"- {Accident.objects.count()} аварий")
    print("Тестовые данные успешно загружены!")
