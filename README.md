# Django Car Registry API

Это Django версия системы регистрации автомобилей, портированная с FastAPI. API предоставляет информацию о транспортных средствах, владельцах, водительских удостоверениях, страховых полисах и авариях.

## Особенности

- **Без авторизации**: Все API endpoints доступны без аутентификации
- **SQLite**: Использует SQLite как основную базу данных (простое развертывание)
- **Django REST Framework**: Современный REST API
- **Swagger документация**: Интерактивная документация API
- **Docker**: Готовая конфигурация для развертывания

## API Endpoints

### 1. Health Check
```
GET /api/health/
```
Проверяет состояние API и подключение к базе данных.

**Ответ:**
```json
{
  "ok": true,
  "database": "connected"
}
```

### 2. Список номерных знаков
```
GET /api/list/
```
Возвращает список всех активных номерных знаков.

**Ответ:**
```json
{
  "plates": ["123ABC02", "456DEF03", ...],
  "count": 1000
}
```

### 3. Проверка по номерному знаку
```
GET /api/check/{plate}/
```
Возвращает полную информацию о транспортном средстве по номерному знаку.

**Пример запроса:**
```
GET /api/check/123ABC02/
```

**Ответ:**
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

## Установка и запуск

### Локальная разработка

1. **Клонируйте репозиторий:**
```bash
cd django_car_registry
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Выполните миграции:**
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Загрузите тестовые данные:**
```bash
python load_data.py
```

5. **Запустите сервер:**
```bash
python manage.py runserver
```

API будет доступен по адресу: `http://localhost:8000/api/`

## 📚 Swagger документация

После запуска сервера доступна интерактивная документация API:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **OpenAPI Schema**: `http://localhost:8000/api/schema/`

Swagger UI позволяет:
- Просматривать все доступные endpoints
- Тестировать API прямо в браузере
- Видеть примеры запросов и ответов
- Изучать структуру данных

### Docker

1. **Запустите с Docker Compose:**
```bash
docker-compose up --build
```

2. **API будет доступен по адресу:** `http://localhost:8000/api/`

## Структура проекта

```
django_car_registry/
├── car_registry/          # Основные настройки Django
│   ├── settings.py        # Настройки проекта
│   ├── urls.py           # Главные URL маршруты
│   └── ...
├── api/                  # Django приложение с API
│   ├── models.py         # Модели базы данных
│   ├── views.py          # API views
│   ├── serializers.py    # DRF сериализаторы
│   ├── urls.py           # API URL маршруты
│   └── admin.py          # Админ панель
├── db/init/              # SQL скрипты для инициализации БД
│   ├── 01_schema.sql     # Схема базы данных
│   ├── 02_seed.sql       # Базовые данные
│   └── 03_mock.sql       # Тестовые данные
├── requirements.txt      # Python зависимости
├── docker-compose.yml    # Docker конфигурация
├── Dockerfile           # Docker образ
└── README.md            # Документация
```

## Модели данных

- **Owner**: Владельцы транспортных средств
- **Vehicle**: Транспортные средства
- **Plate**: Номерные знаки
- **DriverLicense**: Водительские удостоверения
- **Insurer**: Страховые компании
- **InsurancePolicy**: Страховые полисы
- **Accident**: Дорожно-транспортные происшествия

## Админ панель

Django админ панель доступна по адресу: `http://localhost:8000/admin/`

Для создания суперпользователя:
```bash
python manage.py createsuperuser
```

## Отличия от FastAPI версии

1. **Фреймворк**: Django + Django REST Framework вместо FastAPI
2. **ORM**: Django ORM вместо raw SQL запросов
3. **Структура**: Стандартная структура Django проекта
4. **Авторизация**: Полностью убрана (AllowAny для всех endpoints)
5. **CORS**: Настроен для работы с фронтендом

## Технические детали

- **Python**: 3.11+
- **Django**: 4.2.7
- **Django REST Framework**: 3.14.0
- **drf-spectacular**: 0.26.5 (Swagger документация)
- **SQLite**: 3 (встроенная в Python)
- **django-cors-headers**: 4.3.1
