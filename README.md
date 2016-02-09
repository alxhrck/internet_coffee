###Requirements

- Flask
- Celery
- Supervisor
- WiringPi2
- WiringPi2 - gpio
- Redis + Redis python package
- Uwsgi
- Nginx

###Setup
 1. sudo chmod u+s gpio
 2. gpio export 10 out
 
###Run
1. sudo uwsgi --ini coffee.ini -d logs/uwsgi.log
2. /usr/local/bin/celery -A coffee.celery worker
3. supervisord
4. (start) nginx
 
