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
    var time = parseInt($timer.text());
    var correct_links = [];
    for (var i = 0; i < window.picture_links.length; i++) {
        var link = window.picture_links[i];

        function makeSuccessCallback(link) {
            return function() {
                correct_links.push(link);
            }
        }
        var args = {
            url: link,
            type:'HEAD',
            error: function(){},
            success: makeSuccessCallback(link),
        };

        $.ajax(args);
    }  

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
            $("#input-form").submit();
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

    // randomly shuffle indices then get them in a for loop
    var nextLink = function() {
        var link = correct_links[Math.floor(Math.random() * correct_links.length)];
        $('#id_form-BASE_WORD_LINK').attr( 'value', link);
        $('#picture_link_img').attr('src', link); 
    }

    $('#undo-btn').on('click', function(e){
        e.preventDefault();
        if (counter > 0) {
            counter--;
            var last_obj = results.pop();
            var last_obj_ind = results_index.pop();
            $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
            $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
            $('#update_word').text(last_obj['word']);
            $('#picture_link_img').attr('src', last_obj['link']);
        }
    });

    $('#skip-btn').on('click', function(e){
        e.preventDefault();
        skipWord();
    });

    $('#done-btn').on('click', function(){
        window.clearInterval(timeUpdater);
        submitWords();
    });

    $('#yes-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), link: $('#id_form-BASE_WORD_LINK').val(), answer: 1});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextLink();
    });

    $('#no-btn').on('click', function(e){
        e.preventDefault();
        results.push({word: $('#id_form-BASE_WORD').val(), link: $('#id_form-BASE_WORD_LINK').val(), answer: 0});
        results_index.push({word: $('#id_form-BASE_WORD').val(), index: $('#id_form-WORD_INDEX').val()});
        counter++;
        nextLink();
    });

    // TODO: remove the form-0 stuff...
    // 89 is y, 90 is z, 78 is n
    $(document).keydown(function(e) {
        if(e.which === 89) {
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), link: $('#id_form-BASE_WORD_LINK').val(), answer: 1});
            results_index.push({word: $('#id_form-BASE_WORD').val(), link: $('#id_form-BASE_WORD_LINK').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextLink();
        }
        else if(e.which === 78){
            e.preventDefault();
            results.push({word: $('#id_form-BASE_WORD').val(), link: $('#id_form-BASE_WORD_LINK').val(), answer: 0});
            results_index.push({word: $('#id_form-BASE_WORD').val(), link: $('#id_form-BASE_WORD_LINK').val(), index: $('#id_form-WORD_INDEX').val()});
            counter++;
            nextLink();
        }
        if(e.which == 90){
            if (counter > 0) {
                counter--;
                var last_obj = results.pop();
                $('#id_form-BASE_WORD').attr( 'value', last_obj['word']);
                $('#id_form-WORD_INDEX').attr( 'value', last_obj_ind['index']);
                $('#update_word').text(last_obj['word']); 
                $('#picture_link_img').attr('src', last_obj['link']);      
            }
        }

    });

});