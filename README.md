# test_

## О проекте
API на FastAPI с подключенным ботом на Aiogram

**Цели:** 
Основные функции:

- **Получение данных о товаре по артиклю с помощью API**
- **Добавление товара по артикулу в задачу с постоянным обновлением этого товара через каждые 30 минут**

**Эндпоитны:**
- GET docs - Документация проекта.
- POST /api/v1/products BODY {"artikul": ...}, добавление/создание товара в бд.
- GET /api/v1/subscribe/{artikul} - при запросе на который должен запускается сбор данных в бд, но с периодичностью раз в 30 минут.
 
## Стек
- Python 3.11.2
- FastAPI
- Aiogram
- PostgreSQL

## Настройка

### Настройка после клонирования репозитория

После клонирования репозиторий имеет следующую структуру:

```
bim_projects_app
│
├── infta/     # Каталог с файлами инфраструктуры
│   ├── env.example     # Пример конфигурационного файла
│   ├── dev-docker-compose.yml      # Настройки для docker compose
│   └── Dockerfile      # Настройки для Docker
│
├───src/
│   ├───alembic/     # Миграции для основной бд
│   ├───alembic_test/    # Миграции для тестовой бд
│   ├───api/     # Апи
│   │   ├───endpoints
│   │   │   ├── product.py     # роутеры для Продукта
│   │   │   ├── subscribe.py     # роутеры для добавления Продукта в обновление каждые 30 минут
│   │   │   └── __init__.py
│   │   ├── routers.py     # Роутеры для АПИ
│   │   └── __init__.py
│   │
│   ├───core/
│   │   ├── base.py     # Импорт моделей бд для импорта в env.py Alembic
│   │   ├── config.py      # Настройки проекта
│   │   ├── constants.py      # Константы
│   │   ├── db.py      # Настройки бд
│   │   ├── init_db.py      # Логика БД
│   │   ├── logging_.py      # Настройка логгирования
│   │   ├── telegram_bot.py      # Настройка тг приложения
│   │   ├── user.py      # Настройка пользователя
│   │   └── __init__.py
│   │
│   ├───handlers/
│   │   ├── info.py     # Тг хэндлер для получения инфы о боте
│   │   ├── product.py      # Тг хэндлер для получения инфы о продукте по артикулу
│   │   ├── start.py      # Тг хэндлер для инициализации бота
│   │   └── __init__.py
│   │
│   ├───logs
│   │
│   ├───models/
│   │   ├── product.py     # Модель продукта
│   │   ├── user.py      # Модель пользователя
│   │   └── __init__.py
│   │
│   ├───repository/
│   │   ├── base.py     # Базовый репозиторий
│   │   ├── product.py      # Репозиторий продукта
│   │   └── __init__.py
│   │
│   ├───schemas/
│   │   ├── product.py     # Схема продукта
│   │   ├── user.py      # Схема пользователя
│   │   └── __init__.py
│   │
│   ├───services/
│   │   ├── store.py      # Бизнес логика получения продукта через АПИ магазина
│   │   └── __init__.py
│   │
│   ├───text/
│   │   ├── messages.py      # ТГ сообщения
│   │   └── __init__.py
│   │
│   ├── alembic.ini     # Скрипт миграций
│   ├── alembic_test.ini     # Скрипт миграций для тестовой бд
│   ├── Dockerfile      # Докерфайл приложения
│   ├── dockerentrypoint.sh     # Энтрипоинт для запуска приложения в докере
│   ├── main.py     # Базовый файл
│   ├── .gitignore      # Что игнорировать в Git
│   ├── requirements.txt      # Основные зависимости проекта
│   ├── requirements_style.txt      # Зависимости для стилизации кода
│   ├── .pre-commit-config.yaml     # Настройки для проверок перед комитом
│   ├── style.cfg       # Настройки для isort и flake8
│   └── black.cfg       # Настройки для black
│
├── tests/      # Тестирование
|   │   conftest.py     # Тестовые компоненты
│   │   test_api_auth.py     # Тестирование апи аунтефикации
│   │   test_api_product.py     # Тестирование апи продукта
│   │   test_api_subscribe.py       # Тестирование апи задачи каждые 30 минут
│   │   test_services.py        # Тестирование логики
│   │
│   └───fixtures/      # Фикстуры
│           products.py       # Продукты
│           user.py       # Пользователи
│
│   pytest.ini       # настройки pytest
└── README.md       # Этот файл
```
**Устанавливаем и активируем виртуальное окружение**
```
Добавить папку src в рабочую директорию
```
```
Перейти в папку src
```
cd src
```
```shell
python3.11 -m venv .venv
source .venv/bin/activate
```

Устанавливаем зависимости
```shell
pip install -r requirements.txt
pip install -r requirements_style.txt
```

Настраиваем `pre-commit`

```shell
pre-commit install
```

Проверяем, что `pre-commit` работает корректно

```shell
pre-commit run --all-files
```

Возможно потребуется запуск несколько раз. В итоге должен получиться примерно такой вывод:

```shell
trim trailing whitespace............Passed
fix end of files....................Passed
check yaml..........................Passed
check for added large files.........Passed
check for merge conflicts...........Passed
isort...............................Passed
flake8..............................Passed
black...............................Passed
```
#Запуск проекта
Пример .env
```
#  application
NAME_APP="Test application"
SECRET="TestSecretKey"  # Заменить
FIRST_SUPERUSER_EMAIL="test_user@gmail.com"  # Заменить
FIRST_SUPERUSER_PASSWORD="test_password"  # Заменить

#  telegram
TG_TOKEN="testToken"  # Заменить

#  database
POSTGRES_DB="app_db"
POSTGRES_USER="postgress"  # Заменить
POSTGRES_PASSWORD="postgress"  # Заменить
POSTGRES_SERVER="db" # Изменить на название контейнера с БД в Docker Compose
POSTGRES_PORT="5432"

#  test database
TEST_POSTGRES_DB="testbase"
TEST_POSTGRES_USER="postgres"  # Заменить
TEST_POSTGRES_PASSWORD="postgress"  # Заменить
TEST_POSTGRES_SERVER="localhost"  # Изменить на название контейнера развернутой тестовой бд
TEST_POSTGRES_PORT="5432"

#  wildberries
KEY_STORE="testKey"  # Заменить
```
Применить миграции
```
alembic upgrade head
```
Запустить проект через терминал командой
```
python main.py
```
Для развертывания проектка в докере перейдите в папку infra
```
cd ..
cd infra
```
Запустите docker compose
```
docker compose up
```
