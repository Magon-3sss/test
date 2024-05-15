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

const typeofParcelle = document.querySelector('#typeTitle');
const allBtn = document.querySelector('#all');
const holdBtn = document.querySelector('#onHold');
const progressBtn = document.querySelector('#inProgress');
const completedBtn = document.querySelector('#completed');


if(allBtn){
    allBtn.addEventListener('click', writeAll);
}
function writeAll(){
    'use strict'
    typeofParcelle.innerHTML = "All Parcelles";
}


if(holdBtn){
    holdBtn.addEventListener('click', writeHold);
}
function writeHold(){
    'use strict'
    typeofParcelle.innerHTML = "On Hold";
}


if(progressBtn){
    progressBtn.addEventListener('click', writeProgress);
}
function writeProgress(){
    'use strict'
    typeofParcelle.innerHTML = "In Progress";
}


if(completedBtn){
    completedBtn.addEventListener('click', writeCompleted);
}
function writeCompleted(){
    'use strict'
    typeofParcelle.innerHTML = "Completed";
}

