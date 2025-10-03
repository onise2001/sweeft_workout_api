#!/bin/bash
python manage.py migrate
python manage.py seed_exercises
python manage.py runserver 0.0.0.0:8000
