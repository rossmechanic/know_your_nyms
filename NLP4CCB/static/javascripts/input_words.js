/**
 * Created by rossmechanic on 11/29/16.
 */
$(document).ready(function(){
    $('.word-rel-formset').hover(function(){
        $(this).children(".glyphicon").removeClass("hidden");
    }, function(){
        $(this).children(".glyphicon").addClass("hidden");
    });
});