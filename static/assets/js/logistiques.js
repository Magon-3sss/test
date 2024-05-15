/* console.log('permissionsList:', permissionsList);
console.log('hasPermission:', hasPermission); */
// Assurez-vous d'inclure ce script sur les pages où vous souhaitez détecter les changements d'URL

// Fonction pour détecter les changements d'URL
function handleUrlChange() {
    var currentUrl = window.location.href;
  
    // Vérifiez si l'URL a changé
    if (currentUrl !== handleUrlChange.lastUrl) {
        // Affichez la popup ou effectuez d'autres actions ici
        alert('L\'URL a été modifiée!');
  
        // Mettez à jour la dernière URL
        handleUrlChange.lastUrl = currentUrl;
    }
  
    // Vérifiez à intervalles réguliers (par exemple, toutes les secondes)
    setTimeout(handleUrlChange, 1000);
  }
  
  // Initialisez la détection des changements d'URL
  handleUrlChange();

/* function closePopup() {
    document.getElementById('popup').style.display = 'none';
} */

document.addEventListener("DOMContentLoaded", function() {
    fetch('/logistiques')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                window.location.href = "/page-autorisee";
            }
        })
        .catch(error => console.error('Erreur lors de la vérification de l\'accès:', error));
});



const stars = document.querySelectorAll('.star');

for(var i = 0; i < stars.length; i++){
    stars[i].addEventListener('click', activeStar);
}

function activeStar($e){
    'use strict'
    var currentStar = $e.target;

    if(currentStar.classList.contains('active')){
        currentStar.classList.remove('active')
    }
    else{
        currentStar.classList.add('active')
    }
}

const typeofProject = document.querySelector('#typeTitle');
const allBtn = document.querySelector('#all');
const holdBtn = document.querySelector('#onHold');
const progressBtn = document.querySelector('#inProgress');
const completedBtn = document.querySelector('#completed');


if(allBtn){
    allBtn.addEventListener('click', writeAll);
}
function writeAll(){
    'use strict'
    typeofProject.innerHTML = "All Logistiques";
}


if(holdBtn){
    holdBtn.addEventListener('click', writeHold);
}
function writeHold(){
    'use strict'
    typeofProject.innerHTML = "On Hold";
}


if(progressBtn){
    progressBtn.addEventListener('click', writeProgress);
}
function writeProgress(){
    'use strict'
    typeofProject.innerHTML = "In Progress";
}


if(completedBtn){
    completedBtn.addEventListener('click', writeCompleted);
}
function writeCompleted(){
    'use strict'
    typeofProject.innerHTML = "Completed";
}

