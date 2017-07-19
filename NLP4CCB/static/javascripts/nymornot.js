var Cookies = window.Cookies;

$(document).ready(function(){
    var play_set_size = 25
    var $timer = $(".timer");
    var $curr_word = $(".curr_word");
    var word_set = window.word_set['data'];
    var ws_ret = []
    for (var i = 0, len = word_set.length; i < len; i++) {
        ws_ret[i] = word_set[i]['word'];
    }  
    $('#WORD_SET').val(ws_ret.toString());
    var results = [];
    for (var i = 0; i < play_set_size; i++) {
        results[i] = 0;
    }  
    var time = parseInt($timer.text());
    var current = 0;
    var timeUpdater = window.setInterval(function(){
        time -= 1;
        if (time === 0){
            window.clearInterval(timeUpdater);
            submit()
        }
    },1000);

    var timerDOMUpdater = window.setInterval(function(){
        $timer.text(time);
        if (time === 0){
            window.clearInterval(timerDOMUpdater);
        }
    },500);


    $('#false-btn').on('click', function(){
        results[current] = 2
        current += 1;
        $('#RESULTS').val(results.toString());
        if(current == play_set_size){
            window.clearInterval(timeUpdater);
            submit();
        }
        $curr_word.text(word_set[current]['word']);
    });

    $('#true-btn').on('click', function(){
        results[current] = 1
        current += 1;
        $('#RESULTS').val(results.toString());
        if(current == play_set_size){
            window.clearInterval(timeUpdater);
            submit();
        }
        $curr_word.text(word_set[current]['word']);

    });

    $('#undo-btn').on('click', function(){
        if (current > 0) {
            current -= 1;
            results[current] = 0;
            $('#RESULTS').val(results.toString());
            $curr_word.text(word_set[current]['word']);
        }
    });

    var submit = function() {
        $("#input-form").submit();
    };
    $(document).keydown(function(e) {
        if(e.which === 89) {
            results[current] = 1
        }
        else if(e.which === 78){
            results[current] = 2
        }
        else if(e.which == 90){
            if (current > 0) {
                current -= 1;
                results[current] = 0;
                $('#RESULTS').val(results.toString());
                $curr_word.text(word_set[current]['word']);
            }    
        }
        if (e.which === 89 || e.which === 78){
            current += 1;
            $('#RESULTS').val(results.toString());
            if(current == play_set_size){
                window.clearInterval(timeUpdater);
                submit();
            }
            $curr_word.text(word_set[current]['word']);
        }

    });

});