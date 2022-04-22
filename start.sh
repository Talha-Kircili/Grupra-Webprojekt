#!/bin/bash

# gunicorn server
gunicorn -c conf/gunicorn_config.py Grundlagenpraktikum.wsgi
