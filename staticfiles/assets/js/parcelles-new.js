
'use strict';

$(function () {

    $("#ps-datepicker").datepicker({
        autoclose: true,
        format: 'dd-mm-yyyy',
        todayHighlight: true
    }).datepicker('update', new Date());

    $("#pe-datepicker").datepicker({
        autoclose: true,
        format: 'dd-mm-yyyy',
        todayHighlight: true
    }).datepicker('update', '');
});

// Select2
$('.select2').select2({
    minimumResultsForSearch: Infinity,
    width: '100%'
})

// Select2 by showing the search
$('.select2-show-search').select2({
    minimumResultsForSearch: '',
    width: '100%'
})

function selectClient(client) {
    if (!client.id) { return client.text; }
    var $client = $(
        '<span><img src="http://127.0.0.1:8000/static/assets/images/users/' + client.element.value.toLowerCase() + '.jpg" class="rounded-circle avatar-sm" /> '
        + client.text + '</span>'
    );
    return $client;
};

$(".select2-client-search").select2({
    templateResult: selectClient,
    templateSelection: selectClient,
    escapeMarkup: function (m) { return m; }
});

// text editor
$(function (e) {
    $('#summernote').summernote();
});

$(function (e) {
    $('#summernote2').summernote();
});



//display send notifications to client option
const clientCheckbox = document.querySelector('.client-checkbox');
const clientCheckboxContainer = document.querySelector('.client-checkbox-container');
const notificationsContainer = document.querySelector('.notifications-container');
addElementsOnCheck(clientCheckboxContainer, clientCheckbox, notificationsContainer);



//display elements using checkbox
/* function addElementsOnCheck(checkboxContainer, checkboxMain, elementToRemove) {

    checkboxContainer.addEventListener('click', mainFunction);

    function mainFunction() {
        if (checkboxMain.checked == true) {
            elementToRemove.classList.remove('d-none');
        }
        else {
            elementToRemove.classList.add('d-none');
        }
    }
} */