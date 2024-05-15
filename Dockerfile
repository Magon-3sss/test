# Utiliser une version plus récente de Python si disponible
FROM python:3.11.1

# Définir l'environnement en mode non bufferisé
ENV PYTHONUNBUFFERED 1

# Installer les dépendances de l'application
COPY requirements.txt .
RUN pip install -r requirements.txt

# Installer PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib

# Copier les fichiers de l'application
COPY . /app

# Créer le répertoire de l'application
WORKDIR /app

# Configurer PostgreSQL pour l'initialisation de la base de données
RUN service postgresql start && \
    sudo -u postgres psql --command "CREATE USER new WITH SUPERUSER PASSWORD 'new';" && \
    sudo -u postgres createdb -O new new

# Exposer les ports PostgreSQL et Django
EXPOSE 5432 8000

# Définir l'entrypoint pour exécuter le script django.sh
RUN chmod +x /app/django.sh
ENTRYPOINT ["/app/django.sh"]