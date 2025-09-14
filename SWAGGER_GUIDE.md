# Swagger документация API

## 🎯 Что такое Swagger?

Swagger (OpenAPI) - это стандарт для описания REST API, который позволяет:
- Автоматически генерировать интерактивную документацию
- Тестировать API прямо в браузере
- Генерировать клиентские SDK
- Валидировать запросы и ответы

## 📍 Доступ к документации

После запуска сервера доступны следующие URL:

### 1. Swagger UI (рекомендуется)
```
http://localhost:8000/api/docs/
```
- Интерактивный интерфейс
- Возможность тестирования API
- Красивое отображение

### 2. ReDoc
```
http://localhost:8000/api/redoc/
```
- Альтернативный интерфейс
- Более детальная документация
- Лучше для чтения

### 3. OpenAPI Schema (JSON)
```
http://localhost:8000/api/schema/
```
- Машинно-читаемый формат
- Для интеграции с другими инструментами

## 🚀 Как использовать Swagger UI

### 1. Откройте Swagger UI
Перейдите по адресу `http://localhost:8000/api/docs/`

### 2. Изучите endpoints
Вы увидите три группы:
- **Health** - проверка состояния API
- **Plates** - работа с номерными знаками  
- **Vehicles** - информация о транспортных средствах

### 3. Тестируйте API
1. Нажмите на любой endpoint
2. Нажмите "Try it out"
3. Введите параметры (если нужны)
4. Нажмите "Execute"
5. Посмотрите результат

### 4. Примеры использования

#### Проверка здоровья API
```
GET /api/health/
```
- Не требует параметров
- Возвращает статус API и базы данных

#### Получение списка номеров
```
GET /api/list/
```
- Не требует параметров
- Возвращает все активные номерные знаки

#### Проверка по номеру
```
GET /api/check/{plate}/
```
- Требует номерной знак в URL
- Возвращает полную информацию о ТС

## 📋 Структура ответов

### Health Check
```json
{
  "ok": true,
  "database": "connected"
}
```

### Список номеров
```json
{
  "plates": ["123ABC02", "456DEF03"],
  "count": 2
}
```

### Информация о ТС
```json
{
  "plate": "123ABC02",
  "vehicle": {
    "vehicle_id": 1,
    "vin": "WVWZZZ1JZXW000001",
    "make": "Volkswagen",
    "model": "Golf",
    "year": 2019,
    "color": "white"
  },
  "owner": {
    "owner_id": 1,
    "full_name": "Иванов Иван Иванович",
    "iin": "900101123456",
    "dob": "1990-01-01",
    "phone": "+77010000000"
  },
  "driver_license": {
    "license_id": 1,
    "number": "KZ1234567",
    "categories": "B,BE",
    "issued_at": "2020-02-01",
    "expires_at": "2030-02-01",
    "status": "valid"
  },
  "insurance": [
    {
      "policy_number": "OSG-2025-0001",
      "type": "OSAGO",
      "insurer": "Jusan Insurance",
      "valid_from": "2025-01-01",
      "valid_to": "2025-12-31",
      "status": "active"
    }
  ],
  "accidents": [
    {
      "date": "2024-05-10",
      "severity": "minor",
      "location": "Алматы",
      "description": "Столкновение на парковке",
      "fault_party": "other"
    }
  ]
}
```

## 🔧 Настройка Swagger

Swagger настроен в файле `car_registry/settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'Car Registry API',
    'DESCRIPTION': 'API для системы регистрации автомобилей...',
    'VERSION': '1.0.0',
    'TAGS': [
        {'name': 'Health', 'description': 'Проверка состояния API'},
        {'name': 'Plates', 'description': 'Работа с номерными знаками'},
        {'name': 'Vehicles', 'description': 'Информация о транспортных средствах'},
    ],
}
```

## 📝 Документирование новых endpoints

Для добавления документации к новому endpoint используйте декоратор `@extend_schema`:

```python
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

@extend_schema(
    operation_id='my_endpoint',
    summary='Краткое описание',
    description='Подробное описание endpoint',
    tags=['MyTag'],
    parameters=[
        OpenApiParameter(
            name='param',
            type=OpenApiTypes.STR,
            description='Описание параметра'
        )
    ],
    responses={
        200: {
            'description': 'Успешный ответ',
            'examples': {
                'application/json': {
                    'result': 'success'
                }
            }
        }
    }
)
@api_view(['GET'])
def my_endpoint(request):
    # Ваш код
    pass
```

## 🎨 Кастомизация

Вы можете изменить внешний вид Swagger UI, добавив в `SPECTACULAR_SETTINGS`:

```python
SPECTACULAR_SETTINGS = {
    # ... другие настройки
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
    'REDOC_UI_SETTINGS': {
        'hideDownloadButton': False,
        'expandResponses': '200,201',
    },
}
```

## 🚀 Преимущества

1. **Автоматическая документация** - не нужно писать вручную
2. **Интерактивное тестирование** - тестируйте API в браузере
3. **Валидация** - проверка корректности запросов
4. **Генерация клиентов** - автоматическое создание SDK
5. **Стандартизация** - OpenAPI стандарт
