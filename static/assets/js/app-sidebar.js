    // Fonction pour récupérer la valeur d'un cookie par son nom
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Vérifier la présence du jeton JWT
    const jwtToken = getCookie('jwtToken');
    console.log(jwtToken)
    if (jwtToken) {
        const userGroup = getCookie('userGroup') || null;
        const context = {
            jwtToken: jwtToken,
            userGroup: userGroup
        };
        console.log(jwtToken)
        console.log(userGroup)

        // Vous pouvez ici effectuer des actions en fonction du contexte (par exemple, mettre à jour le app-sidebar)
        console.log(context);
    } else {
        // Si le jeton n'est pas présent, rediriger vers la page de connexion
        window.location.href = '/signin';
    }


/* function updateSidebar() {
  const userGroup = getCookie('userGroup');
  const appSidebar = document.getElementById('app-sidebar');

  fetch('/get-sidebar-content/') 
      .then(response => response.json())
      .then(data => {
          appSidebar.innerHTML = data.sidebar_content;
      })
      .catch(error => console.error('Error fetching sidebar content:', error));
}

document.addEventListener('DOMContentLoaded', function() {
  updateSidebar();
});

// Écouter les changements d'URL (par exemple, lorsqu'un lien est cliqué)
window.addEventListener('popstate', function() {
  updateSidebar();
}); */



/* // Get the user's group from the context variable passed to the template
var userGroup = '{{ user_group }}'; // Replace 'user_group' with the actual context variable name

// Show or hide sidebar items based on the user's group
if (userGroup === 'Basic') {
  // Hide parts not accessible to Basic users
  $('.slide-menu').hide(); // Hide all slide menus
  $('.side-menu__item').each(function() {
    var label = $(this).find('.side-menu__label').text();
    if (label !== 'Détection & Analyse' && label !== 'Settings') {
      $(this).hide();
    }
  });
} else if (userGroup === 'Regular') {
  // Hide parts not accessible to Regular users
  $('.slide-menu').hide(); // Hide all slide menus
  $('.side-menu__item').each(function() {
    var label = $(this).find('.side-menu__label').text();
    if (label !== 'Détection & Analyse' && label !== 'Aide à la décision' && label !== 'Réaction' && label !== 'Settings') {
      $(this).hide();
    }
  });
} else if (userGroup === 'Premium') {
  // Hide parts not accessible to Premium users
  $('.slide-menu').hide(); // Hide all slide menus
  $('.side-menu__item').each(function() {
    var label = $(this).find('.side-menu__label').text();
    if (label !== 'Détection & Analyse' && label !== 'Aide à la décision' && label !== 'Réaction' && label !== 'Manegement' && label !== 'Settings') {
      $(this).hide();
    }
  });
} else if (userGroup === 'Advanced') {
  // Hide parts not accessible to Advanced users
  $('.slide-menu').hide(); // Hide all slide menus
  $('.side-menu__item').each(function() {
    var label = $(this).find('.side-menu__label').text();
    if (label !== 'Détection & Analyse' && label !== 'Aide à la décision' && label !== 'Réaction' && label !== 'Manegement' && label !== 'Reporting' && label !== 'IoT' && label !== 'Settings') {
      $(this).hide();
    }
  });
} */


/* var userGroup = getCookie("userGroup");
console.log(userGroup);

document.addEventListener("DOMContentLoaded", function () {
  // Select the elements you want to show/hide based on user group
  var basicElements = document.querySelectorAll(".basic-group");
  var regularElements = document.querySelectorAll(".regular-group");
  var premiumElements = document.querySelectorAll(".premium-group");
  var advancedElements = document.querySelectorAll(".advanced-group");

  // Function to show or hide elements based on user group
  function toggleElements(groupElements) {
    [basicElements, regularElements, premiumElements, advancedElements].forEach(function (elements) {
      elements.forEach(function (element) {
        element.classList.add("hidden"); 
      });
    });

    groupElements.forEach(function (element) {
      element.classList.remove("hidden"); 
    });
  }

  // Show/hide elements based on user group
  if (userGroup === "Basic") {
    toggleElements(userGroup, basicElements);
  } else if (userGroup === "Regular") {
    toggleElements(userGroup, basicElements.concat(regularElements));
  } else if (userGroup === "Premium") {
    toggleElements(userGroup, basicElements.concat(regularElements, premiumElements));
  } else if (userGroup === "Advanced") {
    toggleElements(userGroup, basicElements.concat(regularElements, premiumElements, advancedElements));
  }
}); */


/* document.addEventListener('DOMContentLoaded', function() {
    // Récupérez la valeur du cookie 'userGroup'
    const userGroup = Cookies.get('userGroup');
    console.log(userGroup)

    // Vérifiez le groupe d'utilisateur et ajustez la sidebar en conséquence
    if (userGroup === 'Basic') {
        // Cacher ou afficher des éléments en fonction du groupe Basic
        document.getElementById('calculMenuItem').style.display = 'block';
    } else if (userGroup === 'regular') {
        // Cacher ou afficher des éléments en fonction du groupe regular
        document.getElementById('operationsMenuItem').style.display = 'block';
    }

    // Ajoutez d'autres vérifications ou ajustements en fonction de votre logique
}); */



/* const userGroup = getCookie('userGroup'); // Function to retrieve user group from cookies
const aideDecisionMenu = document.getElementById('aideDecisionMenuItem');

if (userGroup === 'basic') {
  aideDecisionMenu.style.display = 'none'; // Hide the menu item
} else {
  aideDecisionMenu.style.display = 'block'; // Show the menu item
} */

