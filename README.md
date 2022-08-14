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
#### Предстартовые настройки
Файл переменных окружения yatube/yatube/.env_example нужно переименовать в .env и поместить туда необходимую информацию:
- секретный ключ Django SECTRET_KEY, использующийся для хеширования и криптографических подписей. Сгенерировать свой ключ можно, например, на сайте https://djecrety.ir/ либо выполнив в терминале команду:
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```
- информацию относительно PostgreSQL DB
- dsn от sentry.io

По умолчанию проект настроен на PostgreSQL для работы на удаленном сервере. Для локального запуска нужно переключить БД на SQLite, выставив флаг USE_POSTGRES  в положение False в следующей строке в файле yatube/yatube/settings.py:
<br/>
`USE_POSTGRES = False`
<br/>
<br/>
Отключить использование sentry также можно, переведя флаг USE_SENTRY в положение False:
<br/>
`USE_SENTRY = False`

***
#### Start dev app
Клонировать репозиторий и перейти в него в командной строке:
<br/>
`git clone https://github.com/Innis8/Yatube.git`
<br/>
`cd yatube`
<br/>
<br/>
Cоздать и активировать виртуальное окружение:
<br/>
`python -m venv env`
<br/>
`source venv/Scripts/activate`
<br/>
`python -m pip install --upgrade pip`
<br/>
<br/>
Установить зависимости из файла requirements.txt:
<br/>
`pip install -r requirements.txt`
<br/>
<br/>
Выполнить миграции:
<br/>
`python manage.py migrate`
<br/>
<br/>
Запустить сервер:
<br/>
`python manage.py runserver`
<br/>
<br/>
Для отображения статики в settings.py внести изменения:
<br/>
`DEBUG = True`

***
#### Планы на будущее
- Реализовать проект на Docker
