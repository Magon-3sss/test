window.onload = function () {
    const cookies = document.cookie.split(";");

    cookies.forEach(function (cookie) {
    console.log(cookie);
    });
}

  $(document).ready(function() {
    $('#maison-form').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: '/saveMaison/',
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


