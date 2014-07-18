$(document).ready(function() { 
    //Ajax setup for adding csrf header before
    $.ajaxSetup({ 
     beforeSend: function(xhr, settings) {
         function getCookie(name) {
             var cookieValue = null;
             if (document.cookie && document.cookie != '') {
                 var cookies = document.cookie.split(';');
                 for (var i = 0; i < cookies.length; i++) {
                     var cookie = jQuery.trim(cookies[i]);
                     // Does this cookie string begin with the name we want?
                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                     break;
                 }
             }
         }
         return cookieValue;
         }
         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
         }
     } 
    });


    //Verify the field is at least X length long
    function checkLength(value, length) {
        if (value.toString().length < length) { 
            return false;
        }
        else { 
            return true; 
        }
    }

    function flagErrors(field, boolean) {
        selected = "#id_" + field;
        //If there's a length error - flag the box
        if (boolean == true) {
            $(selected).parent().addClass("has-error");            
        }

    }

    //Pre-Post Data Validation
    $('#quoteForm').submit(function (event) {
        event.preventDefault();        
        var the_form = $(this).serializeArray();
        var error_fields = new Array();
        var no_errors = true;

        //Check that the length of each of the required fields is at least 1 character
        for (i=0; i < the_form.length; i++) {
            var name = the_form[i]['name']
            if ( (name != 'csrfmiddlewaretoken') && (name != 'phone')) {                
                //If a field value is less than 2 characters then error it up                
                if ( !checkLength(the_form[i]['value'],2) ) {                     
                    error_fields.push([the_form[i]['name'], true]);
                    no_errors = false;
                }
                else { error_fields.push([the_form[i]['name'], false]); }
            }
        }                        

        //If there are no errors post the info, otherwise hightlight fields
        //EXTRA CAREFUL when changing this - hard-coding the values.
        if (no_errors) {
            $.post("/quote/", { 
                    first_name: the_form[1]['value'], 
                    last_name: the_form[2]['value'], 
                    email: the_form[3]['value'], 
                    phone: the_form[4]['value']} 
                    comments: the_form[5]['value']} 
                );            
        }
        else {
            //Flag all fields that throw errors
            for (i=0; i < error_fields.length;i++) {            
                flagErrors(error_fields[i][0], error_fields[i][1]);    
            }
        }
        

    });


});