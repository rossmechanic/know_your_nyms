/**
 * Created by carriewang
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

    //$('#id_form-0-word').focus();

    var submitWords = function() {
        if (!submitted){
            submitted = true;
            $("#input-form").submit();
            $('.word-rel-formset > input').prop("disabled", true);
        }
    };

    var skipWord = function() {
        //if (!submitted){
        //submitted = true;
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
        //}
    };

    // $('#skip-btn').on('click', function(){
    //    skipWord();
    // });

    $('#undo-btn').on('click', function(){
        window.clearInterval(timeUpdater);
        window.location.href='/models';
    });

    $('#done-btn').on('click', function(){
        window.clearInterval(timeUpdater);
        submitWords();
    });

    $('#true-btn').on('click', function(){
        console.log("yes");
        window.location.href='/models';
    });

    $('#false-btn').on('click', function(){
        console.log("no");
    });

    // TODO: remove the form-0 stuff...
    // 89 is y, 90 is z, 78 is n
    $(document).keydown(function(e) {
        if(e.which === 89) {
            console.log("yes button")
        }
        else if(e.which === 78){
            console.log("no button")
        }
        else if(e.which == 90){
            console.log("back button")   
        }

    });

});