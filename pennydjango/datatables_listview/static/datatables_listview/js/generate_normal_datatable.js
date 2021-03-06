$(document).ready(function () {

    // Buttons definition for the datatable
    try{
        var custom_buttons = custom_buttons;
    }catch(err){
        var custom_buttons = null;
    }
    var final_buttons;
    if(custom_buttons){
        final_buttons = custom_buttons;
    }else{
        final_buttons = [
            {
                extend: 'copy',
                exportOptions: {
                    columns: ':not(:last)'
                },
                text: 'Copy'
            },
            {
                extend: 'csv',
                exportOptions: {
                    columns: ':not(:last)'
                },
                text: 'CSV'
            },
            {
                extend: 'excel',
                exportOptions: {
                    columns: ':not(:last)'
                },
                text: 'Excel'
            },
            {
                extend: 'pdf',
                exportOptions: {
                    columns: ':not(:last)'
                },
                text: 'PDF'
            },

            {
                extend: 'print',
                customize: function (win) {
                    $(win.document.body).addClass('white-bg');
                    $(win.document.body).css('font-size', '10px');

                    $(win.document.body).find('table')
                        .addClass('compact')
                        .css('font-size', 'inherit');
                },
                exportOptions: {
                    columns: ':not(:last)'
                },
                text: 'Imprimir'
            }
        ]
    }

    //==========================================================================================================

    $("#datatable-view").DataTable({
        dom: '<"html5buttons"B>lTfgitp',
        responsive: true,
        bAutoWidth: false,
        pageLength: 10,
        processing: true,
        buttons: final_buttons

    });
});