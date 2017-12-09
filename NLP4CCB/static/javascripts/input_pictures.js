/**
 * Created by carriewang
 */
var Cookies = window.Cookies;

$(document).ready(function(){
    var submitted = false;
    var results = [];
    var results_index = [];
    var counter = 0;
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
            $('#id_form-RESULTS').attr('value', JSON.stringify(results));
            $('#id_form-RESULTS_INDEX').attr('value', JSON.stringify(results_index));
            // array of js objects
            console.log(document.getElementById('id_form-RESULTS').value);
            $("#input-form").submit();
        }
    };

    var nextWord = function() {
        console.log("NEXT WORD");
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
           beforeSend: function(xhr) {
               xhr.setRequestHeader("X-CSRFToken", csrftoken);
           },
            type: "POST",
            url: '/models/pictures_next_word',
            data: {},
            contentType:"application/json",
            success: function(data) {
                $('#id_form-BASE_WORD').attr( 'value', data['base_word']);
                $('#id_form-BASE_WORD_LINK').attr( 'value', data['picture_link']);
                console.log(data['picture_link']);
                $('#picture_link_img').attr('src', data['picture_link']);
                $('#picture_link_img').attr('alt', data['base_word']);
                $('#id_form-WORD_INDEX').attr( 'value', data['word_index']);
                $('#update_word').text(data['base_word']);
            },
            error: function(data) {
                console.log("whoops");
            }
        });
    };

    $('#undo-btn').on('click', function(e){
        e.preventDefault();
        console.log("undo");
        if (counter > 0) {
            counter--;
            var last_obj = results.pop();
            var last_obj_ind = results_index.pop();
            $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
            $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
            $('#update_word').text(last_obj['word']);
            console.log(results);
        }
    });

    $('#done-btn').on('click', function(){
        window.clearInterval(timeUpdater);
        submitWords();
    });

    $('#yes-btn').on('click', function(e){
        e.preventDefault();
        console.log("yes");
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 1});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log(results);
        nextWord();
    });

    $('#no-btn').on('click', function(e){
        e.preventDefault();
        console.log("no");
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 0});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log(results);
        nextWord();
    });

    // TODO: remove the form-0 stuff...
    // 89 is y, 90 is z, 78 is n
    $(document).keydown(function(e) {
        if(e.which === 89) {
            e.preventDefault();
            console.log("yes button");
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 1});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            console.log(results);
            nextWord();
        }
        else if(e.which === 78){
            e.preventDefault();
            console.log("no button");
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 0});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            console.log(results);
            nextWord();
        }
        if(e.which == 90){
            console.log("back button");
            if (counter > 0) {
                counter--;
                var last_obj = results.pop();
                $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
                $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
                $('#update_word').text(last_obj['word']);       
            }
        }

    });

});