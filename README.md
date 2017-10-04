# Загрузка WAV файлов

# Установка проекта
Заранее нужно установить python3.6, pip, virtualenv, git, mysql, libmysqlclient-dev, python-dev, python3-dev
Создать базу mysql

`virtualenv venv -p python3.6`

`source venv/bin/activate`

`cd wav_downloader`

`pip install -r requirements.txt`

`pip install mysqlclient gunicorn`

`cd fileloader`

В файл `main/settings.py` добавить настройки базы данных

`
DATABASES = {

    'default': {
    
        'ENGINE': 'django.db.backends.mysql',
        
        'NAME': 'db_name',
        
        'USER': 'db_user',
        
        'PASSWORD': 'password',
        
        'HOST': 'localhost',
        
        'PORT': '3306',
        
    }
    
}
`

`python manage.py migrate`

`python manage.py collectstatic`

Дальше идет настройка nginx, gunicorn + supervisor 

`http://michal.karzynski.pl/blog/2013/06/09/django-nginx-gunicorn-virtualenv-supervisor/`

Запуск сервера с помощью gunicorn с 3 воркерами
`python gunicorn main.wsgi:application -b 127.0.0.1:8020 --reload -w 3`