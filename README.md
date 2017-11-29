# Загрузка WAV файлов

# Установка проекта
`yum update && yum upgrade`

`yum --enablerepo=extras install epel-release`

`yum install python-pip python-setuptools nginx`

`cd /usr/src`

##### установка Python3.6
```
wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz
tar xzf Python-3.6.1.tgz
cd Python-3.6.1
./configure
make altinstall
cd ..
rm Python-3.6.1.tgz
```

##### установка проекта
```
cd ~
pip install virtualenv
mkdir wav_downloader
cd wav_downloader
virtualenv venv -p python3.6
source venv/bin/activate
git clone https://github.com/skazancev/wav_downloader.git
cd wav_downloader
pip install -r requirements.txt
pip install mysqlclient gunicorn
```

##### создание базы
```
yum install mysql
mysql -uroot -p
```
```
create database wav_downloader character set utf8 collate utf8_general_ci;
CREATE USER 'wav_downloader'@'localhost' IDENTIFIED BY 'password'
GRANT ALL PRIVILEGES ON wav_downloader.* TO 'wav_downloader'@'localhost';
```

##### локальные настройки для проекта
`cd fileloader`

vi main/local.py
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql’,
        'NAME': ‘wav_downloader,
        'USER': 'wav_downloader',
        'PASSWORD': 'password',
        'HOST': '',
        'PORT': '',
    }
}
DEBUG = False
ALLOWED_HOSTS = [‘207.154.254.120’]
```
В local.py можно вносить свои настройки для сервера

    CONFIG_NAME = 'extensions_custom_ivr.conf'
    CONFIG_PATH = '/etc/asterisk/'
    MEDIA_ROOT = '/var/spool/asterisk/sounds/custom/'



##### создание таблиц в базе данных, статика и суперпользователь
```
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser
```

#### запуск проекта как демон
##### установка supervisor
```
pip install supervisor
echo_supervisord_conf > /etc/supervisord.conf
mkdir /etc/supervisord.d/
```

vi /etc/supervisord.conf
Добавить `files = /etc/supervisord.d/*.conf` в секцию `[include]`

в секции `[inet_http_server]` раскомментировать `127.0.0.1:9001`


vi /etc/rc.d/init.d/supervisord
```
#!/bin/sh
#
# /etc/rc.d/init.d/supervisord
#
# Supervisor is a client/server system that
# allows its users to monitor and control a
# number of processes on UNIX-like operating
# systems.
#
# chkconfig: - 64 36
# description: Supervisor Server
# processname: supervisord

# Source init functions
. /etc/rc.d/init.d/functions

prog="supervisord"

prefix="/usr/"
exec_prefix="${prefix}"
prog_bin="${exec_prefix}/bin/supervisord -c /etc/supervisord.conf“
PIDFILE="/var/run/$prog.pid"

start()
{
       echo -n $"Starting $prog: "
       daemon $prog_bin --pidfile $PIDFILE
       [ -f $PIDFILE ] && success $"$prog startup" || failure $"$prog startup"
       echo
}

stop()
{
       echo -n $"Shutting down $prog: "
       [ -f $PIDFILE ] && killproc $prog || success $"$prog shutdown"
       echo
}

case "$1" in

 start)
   start
 ;;

 stop)
   stop
 ;;

 status)
       status $prog
 ;;

 restart)
   stop
   start
 ;;

 *)
   echo "Usage: $0 {start|stop|restart|status}"
 ;;

esac
```

```
chmod +x /etc/rc.d/init.d/supervisord
chkconfig --add supervisord
chkconfig supervisord on
service supervisord start
```
vi /etc/supervisord.d/downloader.conf
```
[program:downloader]
command=/root/wav_downloader/venv/bin/gunicorn main.wsgi:application -b 127.0.0.1:8000 --workers 4 --max-requests 100
directory=/root/wav_downloader/wav_downloader/fileloader/
autostart=true
autorestart=true
redirect_stderr=True
stdout_logfile=/var/log/supervisor/downloader.log
stderr_logfile=/var/log/supervisor/downloader.log
```

```
mkdir /var/log/supervisor && touch /var/log/supervisor/downloader.log
service supervisord restart
```

##### настройка nginx
`yum install nginx`
vi /etc/nginx/conf.d/wav_downloader.conf
```
server {
    listen 80;
    server_name 207.154.254.120;

    location /static/ {
        alias /root/wav_downloader/wav_downloader/static/;
        expires 30;
    }

    location /media/ {
        alias /var/spool/asterisk/sounds/custom/;
        expires 30;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_redirect  off;
        proxy_connect_timeout 90;
        proxy_send_timeout 90;
        proxy_read_timeout 90;
        proxy_buffer_size          4k;
        proxy_buffers              4 32k;
        proxy_busy_buffers_size    64k;
        proxy_temp_file_write_size 64k;
        proxy_temp_path            /etc/nginx/proxy_temp;
    }
}
```

`service nginx reload`
