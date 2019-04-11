$(document).ready(function(){
    //console.log($('div.full-post-content table'));
    $('div.full-post-content table').wrap("<div class='table-container'></div>");
    MathJax.Hub.Queue(["Rerender",MathJax.Hub]);
});

