Requirements

Flask
Celery
WiringPi2
WiringPi2 - gpio
Redis

setup:
$ sudo chmod u+s gpio
# gpio export 10 out
# gpio -g mode 10 out
# gpio -g write 10 1
$ cd internet_coffee/
$ supervisord
