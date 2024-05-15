
(function ($) {
    "use strict";
  
    $('#parcelle-table').DataTable({
      language: {
        searchPlaceholder: 'Search...',
        sSearch: '',
      }
    });
  
    // Select2 
      $('.select2').select2({
          minimumResultsForSearch: Infinity
      });
  
  })(jQuery);
  