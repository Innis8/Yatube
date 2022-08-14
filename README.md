Сервис для публикации блогов Yatube. Возможна регистрация, восстановление пароля по почте, аутентификация по токену, комментирование записей, подписка на авторов и сообщества (объединение блогов в группу по какому-то общему признаку)

***
#### Используемые технологии
- Python 3.7.9
- HTML
- CSS (Bootstrap 3) 
- Django 2.2.16
- Django REST Framework
- Jinja2
- OAuthLib
- sqlite3 (SQLite для тестового локального dev запуска)
- PostgreSQL (для удаленного сервера)
- psycopg2-binary
- SimpleJWT
- gunicorn (для удаленного сервера)
- Nginx (для удаленного сервера)
- Pillow
- Sentry (для удаленного сервера)

***
Файл переменных окружения yatube/yatube/env_example нужно переименовать в .env и поместить туда необходимую информацию:
- секретный ключ Django SECTRET_KEY, использующийся для хеширования и криптографических подписей. Сгенерировать свой ключ можно, например, на сайте https://djecrety.ir/ либо запустив в терминале команду python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
- информацию относительно PostgreSQL DB
- dsn от sentry.io

Пj умолчанию проект настроен на PostgreSQL для работы на удаленном сервере. Для локального запуска нужно переключить БД на SQLite, переименовав дефолтный файл settings.py либо удалив его, и переименовав settings_with_sqlite3.py в settings.py

***
#### Start dev app
Клонировать репозиторий и перейти в него в командной строке:
`
git clone https://github.com/Innis8/Yatube.git
`
`
cd yatube
`

Cоздать и активировать виртуальное окружение:
`
python -m venv env
`
`
source venv/Scripts/activate
`
`
python -m pip install --upgrade pip
`

Установить зависимости из файла requirements.txt:
`
pip install -r requirements.txt
`

Выполнить миграции:
`
python manage.py migrate
`

Запустить сервер:
`
python manage.py runserver
`

Для отображения статики в settings.py внести изменения
`DEBUG = True`

Файл yatube/yatube/env_example нужно переименовать в .env и поместить туда необходимую информацию:
- секретный ключ Django SECTRET_KEY, использующийся для хеширования и криптографических подписей. Сгенерировать свой ключ можно, например, на сайте https://djecrety.ir/ либо запустив в терминале команду:
`python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- информацию относительно PostgreSQL DB (в случае использования этой ДБ на удаленном сервере)
- dsn от sentry.io (в случае использования этой ДБ на удаленном сервере)

***
#### Планы на будущее
- Реализовать проект на Docker