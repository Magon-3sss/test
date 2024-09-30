// Chargez les données d'autorisation depuis le fichier JSON
fetch('/permissions.json')
    .then(response => response.json())
    .then(data => {
        // Utilisez les données pour configurer les autorisations de l'utilisateur
        // Vous devrez implémenter votre propre logique ici en fonction des données.
    });
