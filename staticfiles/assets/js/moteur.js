// Comment out the below code to see the difference.
  $('#modalQuill').on('shown.bs.modal', function() {
    if (map && typeof map.invalidateSize === 'function') {
        map.invalidateSize();
    } else {
        console.error("La carte Leaflet n'est pas correctement initialisée.");
    }
});
  /* $('#modalQuill').on('shown.bs.modal', function() {
    if (map && typeof map.invalidateSize === 'function') {
        map.invalidateSize();
    }    
   });  */

  $(document).ready(function() {
    $('#moteur-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: 'http://localhost:8000/api/saveMoteur/',
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
    typeofProject.innerHTML = "All Moteurs";
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