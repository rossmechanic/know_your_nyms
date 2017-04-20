/**
 * Created by rossmechanic on 2/21/17.
 */
$(document).ready(function(){
    $('#start-button').on('click', function() {
        var $form = $('#rel-type-form');
        if ($form.length){
            $form.submit();
        }
        else {
            $(this).attr("href", "/models/");
        }
    });
});