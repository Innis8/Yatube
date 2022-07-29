после остановки и запуска в другой день виртуальной машины ее ип-адрес меняется. нужно каждый раз вносить этот новый ип в разные места проекта.

settings.py:
hw05_final/yatube/yatube/settings.py
ALLOWED_HOSTS = [новый ип-адрес]
==========
на удаленном сервере:
sudo nano /etc/nginx/sites-enabled/default
server {server_name <ваш-ip>}