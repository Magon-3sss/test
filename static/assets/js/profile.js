$(document).ready(function() {
	$('#image-form').submit(function(event) {
		event.preventDefault();
		var formData = new FormData(this);
		$.ajax({
			url: '/edit-profile',
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

(function ($) {
    "use strict";
    
    // Select2 
	$('.select2').select2({
		minimumResultsForSearch: Infinity
	});

})(jQuery);