#!/usr/bin/env python
"""
Скрипт для тестирования API
"""
import requests
import json

def test_api():
    base_url = "http://localhost:8000/api"
    
    print("=== Тестирование API ===")
    
    # 1. Проверяем health
    print("\n1. Health check:")
    try:
        response = requests.get(f"{base_url}/health/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Получаем список номеров
    print("\n2. Список номерных знаков:")
    try:
        response = requests.get(f"{base_url}/list/")
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Количество номеров: {data['count']}")
        if data['plates']:
            test_plate = data['plates'][0]
            print(f"Тестовый номер: {test_plate}")
            
            # 3. Проверяем конкретный номер
            print(f"\n3. Проверка номера {test_plate}:")
            response = requests.get(f"{base_url}/check/{test_plate}/")
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"ТС: {data['vehicle']['make']} {data['vehicle']['model']}")
                print(f"Владелец: {data['owner']['full_name']}")
                print(f"Количество аварий: {len(data['accidents'])}")
                
                # Проверяем аварии с поврежденными деталями
                for i, accident in enumerate(data['accidents'][:2]):  # Показываем первые 2 аварии
                    print(f"\n  Авария {i+1}:")
                    print(f"    Дата: {accident['date']}")
                    print(f"    Степень: {accident['severity']}")
                    print(f"    Место: {accident['location']}")
                    print(f"    Количество поврежденных деталей: {len(accident['damaged_parts'])}")
                    
                    for part in accident['damaged_parts']:
                        print(f"      - {part['name']} ({part['category']})")
            else:
                print(f"Error: {response.text}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    test_api()
