window.onload = function () {
    // Récupérez le jeton du cookie
    const jwtToken = getCookie('jwtToken');
    console.log('Jetons JWT récupéré sur la page d\'accueil :', jwtToken);
  
    // Vérifiez si le jeton est présent
    if (jwtToken) {
      // Utilisez le jeton comme nécessaire sur la page d'accueil
      console.log("JWT Token:", jwtToken);
  
      // Fonction pour décoder le jeton JWT
      function parseJwt(token) {
        try {
          return JSON.parse(atob(token.split('.')[1]));
        } catch (e) {
          return null;
        }
      }
  
      // Décoder le jeton et afficher le résultat
      var decodedToken = parseJwt(jwtToken);
      console.log("Decoded Token:", decodedToken);
  
      // Accéder aux données du jeton
      if (decodedToken) {
        var userId = decodedToken.user_id;
        console.log("User ID:", userId);
  
        // Ajoutez ces lignes pour récupérer le groupe et les permissions depuis les cookies
        var userGroup = getCookie('group');
        var userPermissions = getCookie('permission');
  
        console.log("User Group:", userGroup);
        console.log("User Permissions:", userPermissions);
      } else {
        console.error("Erreur lors du décodage du jeton.");
      }
    } else {
      console.log('Aucun jeton JWT trouvé sur la page d\'accueil.');
    }
  }

  'use strict';
// Fonction pour récupérer la valeur d'un cookie par son nom
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

  

/*        let jwtToken = null; 

        // Fonction pour obtenir le jeton après l'authentification de l'utilisateur
        function getAuthToken() {
            const userData = {
                username: document.getElementById('username').value,
                password: document.getElementById('password').value,
            };

            fetch('/api/token/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(userData),
            })
            .then((response) => response.json())
            .then((data) => {
                console.log('Réponse du serveur complète :', data);
                jwtToken = data.access;  // Stockez le jeton JWT localement
                const userId = data.user_id;
                const userGroup = data.user_group;
                console.log('Jetons JWT obtenu :', jwtToken);
                console.log('ID de l\'utilisateur :', userId);
                console.log('Groupe de l\'utilisateur :', userGroup);
                document.cookie = `jwtToken=${jwtToken}; secure; path=/`;
                window.location.href = 'index';
            })
            .catch((error) => {
                console.error('Erreur lors de l\'obtention du jeton :', error);
            });
        }

        document.getElementById('loginForm').addEventListener('submit', function (event) {
            event.preventDefault();  
            getAuthToken();  
        }); */