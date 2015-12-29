###Requirements

- Flask
- Celery
- WiringPi2
- WiringPi2 - gpio
- Redis
- Uwsgi
- Nginx

###Setup
 1. sudo chmod u+s gpio
 2. gpio export 10 out
 3. gpio -g mode 10 out
 4. gpio -g write 10 1
 
###Run
1. sudo uwsgi -d --ini coffee.ini
2. supervisord
3. (start) nginx
 
