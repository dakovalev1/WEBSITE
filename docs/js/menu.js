$(document).ready(function(){

    var menu_toggle = false;
    var big_screen = ($("li.menu-button").css("display") == "none");

    $("ul.menu li.menu-button a").click(function(){
        menu_toggle = !menu_toggle;
        $("ul.menu").stop(true);
        if (menu_toggle){
            $("ul.menu").animate({height: "200px"});
        } else {
            $("ul.menu").animate({height: "50px"});
        }
        return false;
    });

    $("ul.menu li.menu-item a").click(function(){
        if (big_screen == false){
            menu_toggle = false;
            $("ul.menu").stop(true);
            $("ul.menu").animate({height: "50px"});
        }
    });

    $(window).resize(function(){
        $("ul.menu").stop(true);
        if ($("li.menu-button").css("display") == "none"){
            $("ul.menu").css("height", "70px");
            menu_toggle = false;
            big_screen = true;
        } else {
            big_screen = false;
            if (menu_toggle){
                $("ul.menu").css("height", "200px");
            } else {
                $("ul.menu").css("height", "50px");
            }
        }
    });
});

