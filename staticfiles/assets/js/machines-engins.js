window.onload = function () {
    const cookies = document.cookie.split(";");

    cookies.forEach(function (cookie) {
    console.log(cookie);
    });
    /* const jwtToken = document.cookie;

        console.log(jwtToken) */ 

    /* var token='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY5OTk1MzczNSwiaWF0IjoxNjk5ODY3MzM1LCJqdGkiOiIxYjdkOTU0ODkyMzg0NjQ4OWE1MGRkZGY3YzM3M2YyOSIsInVzZXJfaWQiOjI0fQ.CJqK8hcvvt2oBY6HIZW0O5037jZQtsO7bpOLOszZZ2g';
    var base64Url = token.split('.')[1];
    var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    var jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));

    console.log(JSON.parse(jsonPayload)); */
}
getAuthToken(); // Obtenez le jeton JWT au chargement de la page
function init() {
    const allocationCheckbox = document.getElementById('allocation');
    const prixLocationSection = document.getElementById('prix-location');
    const prixAchatSection = document.getElementById('prix-achat');
  
    allocationCheckbox.addEventListener('change', function() {
      if (this.checked) {
        prixLocationSection.style.display = 'block';
        prixAchatSection.style.display = 'none';
        document.getElementById('date-achat').value="";
        document.getElementById('achat').value=null;
      } else {
        prixLocationSection.style.display = 'none';
        prixAchatSection.style.display = 'block';
        document.getElementById('date-location').value="";
        document.getElementById('prix-mois').value=null;
        document.getElementById('prix-jour').value=null;
        document.getElementById('prix-heure').value=null;
      }
    });

$(document).ready(function() {
    $('#machine-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        const jwtToken = document.cookie.match(/jwtToken=([^;]+)/)[1];

        //var jwtToken = getCookie('jwt_token');
        //var jwtToken = getJwtToken('jwt_token'); 
        console.log(jwtToken)

        if (jwtToken) {
            $.ajax({
                url: 'saveMachine/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                headers: {
                    'Authorization': 'Bearer ' + jwtToken,   
                }, 
                success: function(data) {
                    // Handle success response
                    console.log(data);
                    location.reload();
                },
                error: function(xhr, textStatus, errorThrown) {
                    // Handle error response
                    console.log(xhr.responseText);
                }
            });
        } 
        else {
            window.location.href = 'signin';
        }
    });
});
    
}

function getJwtToken() {
    const cookies = document.cookie.split(';');
    console.log(cookies);
    for (const cookie of cookies) {
        console.log(cookies);
      const [name, value] = cookie.split('=');
      if (name === 'jwt_token') {
        return value;
      }
    }
    return null; 
  } 

/* window.onload = init; */

 



/* function goToAddMachine(event) {
    event.preventDefault();
    var group = localStorage.getItem('group');
    if (group !== 'Basic' && group !== 'Premium' && group !== 'Advanced') {
        window.location.href = 'logistiques';
        return; 
    }

    // Get the machine form
    const form = $('#machine-form');

    // Submit the machine form
    form.submit();
} */



function displayIcon(input) {
    const icon = input.parentNode.querySelector(".icon");

    icon.style.display = "inline-block";

    input.addEventListener("mouseleave", function() {
        icon.style.display = "none";
    });
}


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