$(document).ready(function(){

    var menu_toggle = false;

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
        menu_toggle = false;
        $("ul.menu").css("height", "50px");
    });

    $(window).resize(function(){
        if ($("li.menu-button").css("display") == "none"){
            $("ul.menu").stop(true);
            $("ul.menu").css("height", "70px");
            menu_toggle = false;
        } else {
            if (menu_toggle){
                $("ul.menu").css("height", "200px");
            } else {
                $("ul.menu").css("height", "50px");
            }
        }
    });
});

