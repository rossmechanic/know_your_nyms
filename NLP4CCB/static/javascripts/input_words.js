/**
 * Created by rossmechanic on 11/29/16.
 */
var Cookies = window.Cookies;

$(document).ready(function(){
    var submitted = false;
    var $timer = $(".timer");
    var time = parseInt($timer.text())
    var timeUpdater = window.setInterval(function(){
        time -= 1;
        if (time === 0){
            window.clearInterval(timeUpdater);
            submitWords();
        }
    },1000);

    var timerDOMUpdater = window.setInterval(function(){
        $timer.text(time);
        if (time === 0){
            window.clearInterval(timerDOMUpdater);
        }
    },500);

    $('#id_form-0-word').focus();

    var submitWords = function() {
        if (!submitted){
            submitted = true;
            $("#input-form").submit();
            $('.word-rel-formset > input').prop("disabled", true);
        }
    };

    var skipWord = function() {
        if (!submitted){
            submitted = true;
            var csrftoken = Cookies.get('csrftoken');
            $.ajax({
               beforeSend: function(xhr) {
                   xhr.setRequestHeader("X-CSRFToken", csrftoken);
               },
                type: "POST",
                url: '/models/',
                data: {skip: 'true', sem_rel: $('#id_form-SEM_REL').val(), base_word: $('#id_form-BASE_WORD').val(), word_index: $('#id_form-WORD_INDEX').val()},
                success: function() {
                    window.location.href='/models';
                }
            });
        }
    };

    $('#skip-btn').on('click', function(){
       skipWord();
    });

    $('#done-btn').on('click', function(){
        window.clearInterval(timeUpdater);
        submitWords();
    });

    // 9 is tab; 13 is enter
    $(document).on('keydown','.word-rel-formset', function(event){
        if ((event.which === 9 || event.which === 13) && $(this).is(':last-child')) {
            event.preventDefault();
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
            $(this).next().find('input').focus();
            var numForms = parseInt($('#id_form-TOTAL_FORMS').val()) + 1;
            $('#id_form-TOTAL_FORMS').val(String(numForms));
        }

    });

});