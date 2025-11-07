#!/bin/sh
set -e
gunicorn wedding_website.wsgi:application --log-file -