window.onload = function () {
    
} 

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

  function saveOutil(){
    console.log("click event !");
} 

$(document).ready(function() {
    $('#outil-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/saveOutil/',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
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
    });
});


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


