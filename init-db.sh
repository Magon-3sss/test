#!/bin/bash

# Démarrer PostgreSQL en arrière-plan
service postgresql start

# Attendre que PostgreSQL démarre
sleep 5

# Configurer la base de données
psql -U postgres -c "CREATE USER new WITH SUPERUSER PASSWORD 'new';"
psql -U postgres -c "CREATE DATABASE new OWNER new;"

# Exécuter les migrations et démarrer le serveur Django
./django.sh
