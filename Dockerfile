# Utiliser une version plus récente de Python si disponible
FROM python:3.11.1

# Définir l'environnement en mode non bufferisé
ENV PYTHONUNBUFFERED 1

# Créer le répertoire de l'application
WORKDIR /app

# Installer les dépendances de l'application
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copier les fichiers de l'application
COPY . .

# Exposer le port utilisé par l'application
EXPOSE 8000
RUN chmod +x /app/django.sh
# Définir l'entrypoint pour exécuter le script django.sh
ENTRYPOINT ["./django.sh"]