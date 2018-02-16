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

    //$('#id_form-0-word').focus();

    var submitWords = function() {
        if (!submitted){
            submitted = true;
            $('#id_form-RESULTS').attr('value', JSON.stringify(results));
            $('#id_form-RESULTS_INDEX').attr('value', JSON.stringify(results_index));
            $("#input-form").submit();
        }
    };

    var nextWord = function() {
        var csrftoken = Cookies.get('csrftoken');
        $.ajax({
           beforeSend: function(xhr) {
               xhr.setRequestHeader("X-CSRFToken", csrftoken);
           },
            type: "POST",
            url: '/models/concrete_next_word',
            data: {},
            contentType:"application/json",
            success: function(data) {
                $('#id_form-BASE_WORD').attr( 'value', data['base_word']);
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
        if (counter > 0) {
            counter--;
            var last_obj = results.pop();
            var last_obj_ind = results_index.pop();
            $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
            $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
            $('#update_word').text(last_obj['word']);
        }
    });

    $('#done-btn').on('click', function(){
        window.clearInterval(timeUpdater);
        submitWords();
    });

    $('#one-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 1});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextWord();
    });

    $('#two-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 2});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextWord();
        //window.location.href='/models';
    });

    $('#three-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 3});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextWord();
        //window.location.href='/models';
    });

    $('#four-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 4});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextWord();
        //window.location.href='/models';
    });

    $('#five-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 5});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextWord();
        //window.location.href='/models';
    });

    // TODO: remove the form-0 stuff...
    // 89 is y, 90 is z, 78 is n
    $(document).keydown(function(e) {

        if(e.which === 90){
            if (counter > 0) {
                counter--;
                var last_obj = results.pop();
                var last_obj_ind = results_index.pop();
                $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
                $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
                $('#update_word').text(last_obj['word']);       
            }
        }

        //1
        else if(e.which === 97 || e.which === 49) {
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 1});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextWord();
        }

        //2
        else if (e.which === 98 || e.which === 50) {
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 2});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextWord();
        }

        //3
        else if (e.which === 99 || e.which === 51) {
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 3});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextWord();
        }

        //4
        else if (e.which === 100 || e.which === 52) {
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 4});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextWord();
        }

        //5
        else if (e.which === 101 || e.which === 53) {
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), answer: 5});
            results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextWord();
        }

    });

});