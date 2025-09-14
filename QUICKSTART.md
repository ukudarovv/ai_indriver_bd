# Быстрый старт Django Car Registry API

## 🚀 Запуск проекта

### Вариант 1: Локальный запуск

1. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

2. **Выполните миграции:**
```bash
python manage.py migrate
```

3. **Загрузите тестовые данные:**
```bash
python load_data.py
```

4. **Запустите сервер:**
```bash
python manage.py runserver
```

### Вариант 2: Docker (рекомендуется)

1. **Запустите с Docker Compose:**
```bash
docker-compose up --build
```

## 📡 API Endpoints

После запуска API будет доступно по адресу: `http://localhost:8000/api/`

## 📚 Swagger документация

После запуска сервера доступна интерактивная документация:

- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`

В Swagger UI можно тестировать API прямо в браузере!

### Основные endpoints:

- **Health Check:** `GET /api/health/`
- **Список номеров:** `GET /api/list/`
- **Проверка по номеру:** `GET /api/check/{plate}/`

### Примеры запросов:

```bash
# Проверка здоровья API
curl http://localhost:8000/api/health/

# Получение списка номерных знаков
curl http://localhost:8000/api/list/

# Проверка конкретного номера (замените на реальный номер из списка)
curl http://localhost:8000/api/check/123ABC02/
```

## 🔧 Админ панель

Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

Админ панель: `http://localhost:8000/admin/`

## 📊 Тестовые данные

Скрипт `load_data.py` создает:
- 100 владельцев с водительскими удостоверениями
- 100 транспортных средств с номерными знаками
- Страховые полисы (OSAGO и KASKO)
- Случайные аварии

## 🐛 Устранение проблем

### Ошибка подключения к базе данных
- SQLite создается автоматически, проверьте права доступа к папке проекта

### Ошибки миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### Очистка и пересоздание данных
```bash
python load_data.py
```

## 📝 Структура проекта

```
django_car_registry/
├── api/                    # Django приложение
│   ├── models.py          # Модели базы данных
│   ├── views.py           # API views
│   ├── serializers.py     # DRF сериализаторы
│   └── urls.py           # API маршруты
├── car_registry/          # Настройки Django
├── db/init/              # SQL скрипты
├── requirements.txt      # Зависимости
├── docker-compose.yml    # Docker конфигурация
└── README.md            # Полная документация
```
