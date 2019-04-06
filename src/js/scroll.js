var target = window.location.hash,
target = target.replace('#', '');
window.location.hash = "";



$(document).ready(function(){
    
    function scroll(elem){
        if (elem.length == 1){
            var offset = 0;
            
            if ($("li.menu-button").css("display") == "none"){
                offset = 70;
            } else {
                offset = 50;
            }

            $('html, body').stop(true);
            $('html, body').animate({
                scrollTop: elem.offset().top - offset
            }, 800);
        }
    }


    var elem = $("a[name=\'" + target + "\']");
    scroll(elem);


    $("a.hashtag").click(function(){

        var hash = $(this).attr("href");
        hash = hash.replace("#", "");
        
        var elem = $("a[name=\'" + hash + "\']");

        scroll(elem);
        return false;
    });
});

