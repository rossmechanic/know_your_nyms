/**
 * Created by rossmechanic on 11/29/16.
 */
$(document).ready(function(){
    console.log("READY");
    var $timer = $(".timer");
    var time = parseInt($timer.text())
    var timeUpdater = window.setInterval(function(){
        time -= 1;
        if (time === 0){
            window.clearInterval(timeUpdater);
            console.log("SUBMIT");
            submitWords();
        }
    },1000);

    var timerDOMUpdater = window.setInterval(function(){
        $timer.text(time);
        if (time === 0){
            window.clearInterval(timerDOMUpdater);
        }
    },500);

    var submitWords = function() {
        $.post('./scoring/',$('#input-form, .word-rel-formset :input').serialize(), function(data) {
            console.log(data);
        });
        $('.word-rel-formset > input').prop("disabled", true);
    }

    $(document).on('keydown','.word-rel-formset', function(event){
        if (event.which === 9 && $(this).is(':last-child')) {
            var newIndex = String(parseInt(this.getAttribute("index")) + 1);
            $(this).after(
                "<div class='form-group word-rel-formset' index = " + newIndex +
                ">" +
                "<input " +
                "id='id_form-" + newIndex + "-word'" +
                "maxlength='100'" +
                "name='form-" + newIndex + "-word'" +
                "type='text'" +
                ">" +
                "</div>"
            );

            var numForms = parseInt($('#id_form-TOTAL_FORMS').val()) + 1;
            $('#id_form-TOTAL_FORMS').val(String(numForms));
        }

    });

});