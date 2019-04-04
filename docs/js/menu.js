$(document).ready(function(){

    var menu_toggle = false;

    $("ul.menu li.menu-button a").click(function(){
        if (menu_toggle){
            $("ul.menu").css("height", "50px");
        } else {
            $("ul.menu").css("height", "200px");
        }
        menu_toggle = !menu_toggle;
        return false;
    });
    
    $("ul.menu li.menu-item a").click(function(){
        menu_toggle = false;
        $("ul.menu").css("height", "50px");
    });
});

