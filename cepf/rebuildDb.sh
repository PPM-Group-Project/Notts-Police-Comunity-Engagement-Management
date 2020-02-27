#!/bin/bash

find -name "migrations" -exec rm -rf \;
rm db.sqlite3
python3 manage.py makemigrations community
python3 manage.py makemigrations management
python3 manage.py migrate
