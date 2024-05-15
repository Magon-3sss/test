#!/bin/bash
echo "Starting PostgreSQL..."
service postgresql start

echo "Creating Migrations..."
python manage.py makemigrations app
echo ====================================

echo "Starting Migrations..."
python manage.py migrate
echo ====================================

echo "Starting Server..."
python manage.py runserver 0.0.0.0:8000