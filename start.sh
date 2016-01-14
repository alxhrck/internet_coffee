#!/bin/bash
sudo uwsgi --ini coffee.ini -d logs/uwsgi.log
supervisord
