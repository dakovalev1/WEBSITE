var target = window.location.hash,
target = target.replace('#', '');
window.location.hash = "";



$(document).ready(function(){
    var elem = $("a[name=\'" + target + "\']");
    if (elem.length == 1){
        $('html, body').animate({
            scrollTop: elem.offset().top - 50
          }, 800);
    }


    $("a.hashtag").click(function(){
        var hash = $(this).attr("href");
        hash = hash.replace("#", "");
        
        var elem = $("a[name=\'" + hash + "\']");

        var offset = 0;

        if ($("li.menu-button").css("display") == "none"){
            offset = 70;
        } else {
            offset = 50;
        }
        
        $('html, body').animate({
            scrollTop: elem.offset().top - offset
          }, 800);
        return false;
    });
});

