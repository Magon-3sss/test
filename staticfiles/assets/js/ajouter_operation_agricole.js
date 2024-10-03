window.onload = function () {
         
}


/* 
  function save_operation(){
    console.log("click event !");
}


$(document).ready(function() {
    $('#operation').submit(function(event) {
        event.preventDefault();
        var formData = new FormData(this);
        $.ajax({
            url: 'http://localhost:8000/api/save_operation/',
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
}); */
document.addEventListener("DOMContentLoaded", function() {
    // Fonction pour sauvegarder les données d'une étape
    function saveStepData(step) {
      const stepData = {};
      // Collecter les données de tous les champs de l'étape
      document.querySelectorAll(`#step-${step} input, #step-${step} select, #step-${step} textarea`).forEach(input => {
        stepData[input.name] = input.value;
      });
      // Sauvegarder les données dans le local storage
      localStorage.setItem(`step-${step}-data`, JSON.stringify(stepData));
    }
  
    // Écouteurs d'événements pour les boutons "Next"
    document.querySelectorAll(".next-btn").forEach(button => {
      button.addEventListener("click", function() {
        const step = this.dataset.step;
        saveStepData(step);
        // Passer à l'étape suivante (à implémenter selon votre logique)
        const nextStep = parseInt(step) + 1;
        document.querySelector(`#step-${step}`).style.display = 'none';
        document.querySelector(`#step-${nextStep}`).style.display = 'block';
      });
    });
});


      function submitStep1() {
          const form = document.getElementById('step-10');
          const formData = new FormData(form);

          fetch('/step1/', {
              method: 'POST',
              body: formData,
          })
          .then(response => response.json())
          .then(data => {
              if (data.errors) {
                  alert('Error: ' + JSON.stringify(data.errors));
              } else {
                  document.getElementById('step-10').style.display = 'none';
                  document.getElementById('step-11').style.display = 'block';
              }
          })
          .catch(error => console.error('Error:', error));
      }

      function submitStep2() {
          const form = document.getElementById('step-11');
          const formData = new FormData(form);

          fetch('/step2/', {
              method: 'POST',
              body: formData,
          })
          .then(response => response.json())
          .then(data => {
              if (data.errors) {
                  alert('Error: ' + JSON.stringify(data.errors));
              } else {
                  document.getElementById('step-11').style.display = 'none';
                  document.getElementById('step-12').style.display = 'block';
              }
          })
          .catch(error => console.error('Error:', error));
      }
      function submitStep3() {
        const form = document.getElementById('step-12');
        const formData = new FormData(form);

        fetch('/step2/', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.errors) {
                alert('Error: ' + JSON.stringify(data.errors));
            } else {
                document.getElementById('step-12').style.display = 'none';
                document.getElementById('step-13').style.display = 'block';
            }
        })
        .catch(error => console.error('Error:', error));
    }
  
  function submitStep4() {
    const form = document.getElementById('step-13');
    const formData = new FormData(form);

    fetch('/step2/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Error: ' + JSON.stringify(data.errors));
        } else {
            document.getElementById('step-13').style.display = 'none';
            document.getElementById('step-14').style.display = 'block';
        }
    })
    .catch(error => console.error('Error:', error));
}
function submitStep5() {
  const form = document.getElementById('step-14');
  const formData = new FormData(form);

  fetch('/step2/', {
      method: 'POST',
      body: formData,
  })
  .then(response => response.json())
  .then(data => {
      if (data.errors) {
          alert('Error: ' + JSON.stringify(data.errors));
      } else {
          document.getElementById('step-14').style.display = 'none';
          document.getElementById('step-15').style.display = 'block';
      }
  })
  .catch(error => console.error('Error:', error));
}
function submitStep6() {
const form = document.getElementById('step-15');
const formData = new FormData(form);

fetch('/step2/', {
    method: 'POST',
    body: formData,
})
.then(response => response.json())
.then(data => {
    if (data.errors) {
        alert('Error: ' + JSON.stringify(data.errors));
    } else {
        document.getElementById('step-15').style.display = 'none';
        document.getElementById('step-16').style.display = 'block';
    }
})
.catch(error => console.error('Error:', error));
}

function submitStep7() {
const form = document.getElementById('step-16');
const formData = new FormData(form);

fetch('/step2/', {
    method: 'POST',
    body: formData,
})
.then(response => response.json())
.then(data => {
    if (data.errors) {
        alert('Error: ' + JSON.stringify(data.errors));
    } else {
        document.getElementById('step-16').style.display = 'none';
        document.getElementById('step-17').style.display = 'block';
    }
})
.catch(error => console.error('Error:', error));
}

function submitStep8() {
const form = document.getElementById('step-17');
const formData = new FormData(form);

fetch('/step2/', {
    method: 'POST',
    body: formData,
})
.then(response => response.json())
.then(data => {
    if (data.errors) {
        alert('Error: ' + JSON.stringify(data.errors));
    } else {
        document.getElementById('step-17').style.display = 'none';
        document.getElementById('step-18').style.display = 'block';
    }
})
.catch(error => console.error('Error:', error));
}

function submitStep9() {
const form = document.getElementById('step-18');
const formData = new FormData(form);

fetch('/step2/', {
    method: 'POST',
    body: formData,
})
.then(response => response.json())
.then(data => {
    if (data.errors) {
        alert('Error: ' + JSON.stringify(data.errors));
    } else {
        document.getElementById('step-18').style.display = 'none';
        document.getElementById('step-19').style.display = 'block';
    }
})
.catch(error => console.error('Error:', error));
}

function submitStep9() {
    const form = document.getElementById('step-19');
    const formData = new FormData(form);
    
    fetch('/step2/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Error: ' + JSON.stringify(data.errors));
        } else {
            document.getElementById('step-19').style.display = 'none';
            document.getElementById('Enregistrer').style.display = 'block';
        }
    })
    .catch(error => console.error('Error:', error));
    }
 
(function($) {
    "use strict" ;

    // Toolbar extra buttons
    var btnFinish = $('<button></button>').text('Finish')
        .addClass('btn btn-secondary')
        .on('click', function(){ 
            $('#operation').submit(); 
        });
    var btnCancel = $('<button></button>').text('Cancel')
        .addClass('btn btn-secondary')
        .on('click', function(){ 
            $('#smartwizard-3').smartWizard("reset"); 
        });

    $('#smartwizard-3').smartWizard({
        selected: 0,
        theme: 'dots',
        transitionEffect: 'fade',
        showStepURLhash: false,
        toolbarSettings: {
            toolbarButtonPosition: 'end',
            toolbarExtraButtons: [btnFinish, btnCancel]
        }
    });
    
    /* $(document).ready(function() {
        $('#operation').submit(function(event) {
            event.preventDefault();
            
            var formData = new FormData(this);
    
            // Ensure required fields are included
            var project_id = $('#geozone').val();  // Assuming `geozone` dropdown contains project_id
            var typeoperation = $('#typeoperation').val();
    
            if (!project_id || !typeoperation) {
                alert("Project and operation type are required!");
                return;
            }
    
            $.ajax({
                url: 'http://localhost:8000/api/save_operation/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    console.log(data);
                    alert('Operation saved successfully!');
                },
                error: function(xhr, textStatus, errorThrown) {
                    console.log(xhr.responseText);
                    alert("Error: " + xhr.responseText);
                }
            });
        });
    }); */
    
    $(document).ready(function() {
        $('#operation').submit(function(event) {
            event.preventDefault();
            var formData = new FormData(this);
            $.ajax({
                url: 'save_operation/',
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

    
    
})(jQuery);