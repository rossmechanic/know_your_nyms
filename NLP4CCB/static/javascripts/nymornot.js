var Cookies = window.Cookies;

$(document).ready(function(){
    var $timer = $(".timer");
    var $curr_word = $(".curr_word");
    var word_set = window.word_set['data'];
    var ws_ret = []
    for (var i = 0, len = word_set.length; i < len; i++) {
        ws_ret[i] = word_set[i]['word'];
    }  
    $('#WORD_SET').val(ws_ret.toString());
    var results = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];
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
        console.log(word_set[current]['word'])
        $('#RESULTS').val(results.toString());
        if(current == 25){
            window.clearInterval(timeUpdater);
            submit();
        }
        $curr_word.text(word_set[current]['word']);
    });

    $('#true-btn').on('click', function(){
        results[current] = 1
        current += 1;
        console.log(word_set[current]['word'])
        $('#RESULTS').val(results.toString());
        if(current == 25){
            window.clearInterval(timeUpdater);
            submit();
        }
        $curr_word.text(word_set[current]['word']);

    });

    var submit = function() {
        $("#input-form").submit();
    };
    $(document).keydown(function(e) {
        if(e.which === 74) {
            results[current] = 1
        }
        else if(e.which === 70){
            results[current] = 2
        }
        if (e.which === 74 || e.which === 70){
            current += 1;
            console.log(word_set[current]['word'])
            $('#RESULTS').val(results.toString());
            if(current == 25){
                window.clearInterval(timeUpdater);
                submit();
            }
            $curr_word.text(word_set[current]['word']);
        }

    });

});