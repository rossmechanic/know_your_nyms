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
            // array of js objects
            console.log(document.getElementById('id_form-RESULTS').value);
            $("#input-form").submit();
            //$('.word-rel-formset > input').prop("disabled", true);
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
            url: '/models/concrete_next_word',
            data: {},
            contentType:"application/json",
            //data: {skip: 'true', sem_rel: $('#id_form-SEM_REL').val(), base_word: $('#id_form-BASE_WORD').val(), word_index: $('#id_form-WORD_INDEX').val()},
            success: function(data) {
                //console.log("data "+ data["base_word"]);
                //$('#id_form-BASE_WORD').val() = data["base_word"];
                //console.log(document.getElementById("id_form-BASE_WORD").attributes['value']);
                //document.getElementById("id_form-BASE_WORD").attributes['value'] = data["base_word"];
                $('#id_form-BASE_WORD').attr( 'value', data['base_word']);
                $('#id_form-WORD_INDEX').attr( 'value', data['word_index']);
                $('#update_word').text(data['base_word']);
            },
            error: function(data) {
                console.log("whoops");
            }
        });
        //}
    };

    // $('#skip-btn').on('click', function(){
    //    skipWord();
    // });

    $('#undo-btn').on('click', function(e){
        //window.clearInterval(timeUpdater);
        e.preventDefault();
        console.log("undo");
        if (counter > 0) {
            counter--;
            var last_obj = results.pop();
            var last_obj_ind = results_index.pop();
            //document.getElementById("id_form-BASE_WORD").attributes['value'] = last_obj['word'];
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

    $('#one-btn').on('click', function(e){
        e.preventDefault();
        console.log("1");
        //window.location.href='/models';
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 1});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log("1");
        console.log(results);
        console.log(results_index);
        nextWord();
    });

    $('#two-btn').on('click', function(e){
        e.preventDefault();
        console.log("2");
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 2});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log("2");
        console.log(results);
        console.log(results_index);
        nextWord();
        //window.location.href='/models';
    });

    $('#three-btn').on('click', function(e){
        e.preventDefault();
        console.log("3");
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 3});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log("3");
        console.log(results);
        console.log(results_index);
        nextWord();
        //window.location.href='/models';
    });

    $('#four-btn').on('click', function(e){
        e.preventDefault();
        console.log("4");
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 4});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log("4");
        console.log(results);
        console.log(results_index);
        nextWord();
        //window.location.href='/models';
    });

    $('#five-btn').on('click', function(e){
        e.preventDefault();
        console.log("5");
        results.push({word: $('#id_form-BASE_WORD').val(), answer: 5});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        console.log("5");
        console.log(results);
        console.log(results_index);
        nextWord();
        //window.location.href='/models';
    });

    // TODO: remove the form-0 stuff...
    // 89 is y, 90 is z, 78 is n
    $(document).keydown(function(e) {
        // if(e.which === 89) {
        //     e.preventDefault();
        //     console.log("yes button");
        //     results.push({word: $('#id_form-BASE_WORD').val(), answer: 1});
        //     counter++;
        //     nextWord();
        // }
        // else if(e.which === 78){
        //     e.preventDefault();
        //     console.log("no button");
        //     results.push({word: $('#id_form-BASE_WORD').val(), answer: 0});
        //     counter++;
        //     nextWord();
        // }
        if(e.which == 90){
            console.log("back button");
            if (counter > 0) {
                counter--;
                var last_obj = results.pop();
                var last_obj_ind = results_index.pop();
                $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
                $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
                $('#update_word').text(last_obj['word']);       
            }
        }

    });

});