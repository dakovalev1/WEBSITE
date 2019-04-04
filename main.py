import os
import shutil
import markdown
import configparser
import numpy
import lxml.html as html
import lxml.html.builder as builder

def make_head():
    head = [
        builder.META(charset="utf-8"),
        builder.TITLE("Author Name"),
        builder.META(name="viewport", content = "width=device-width, initial-scale=1"),
        builder.SCRIPT("", type="text/javascript", src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js",async="async"),
        builder.SCRIPT("MathJax.Hub.Config({" +
            "config: [\"MMLorHTML.js\"], "+
            "jax: [\"input/TeX\", \"output/HTML-CSS\", \"output/NativeMML\"], "+
            "extensions: [\"MathMenu.js\", \"MathZoom.js\"]});",
            type="text/x-mathjax-config"),
        builder.SCRIPT("", src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
        builder.SCRIPT("", src="js/jquery.waypoints.min.js"),
        builder.SCRIPT("", src="js/jquery.scrollTo.min.js"),
        builder.LINK(rel="stylesheet",
            href="https://use.fontawesome.com/releases/v5.8.1/css/all.css",
            integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
            crossorigin="anonymous")
    ]

    return head
def make_menu():
    menu = builder.UL(
        builder.LI(builder.A(builder.I("", builder.CLASS("fas fa-bars")), href=""), builder.CLASS("menu-button")),
        builder.LI(builder.A(builder.B("Author Name"), href="index.html"), builder.CLASS("menu-title")),
        builder.LI(builder.A(builder.B("Home"), href="index.html#home.page-section"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Posts"), href="index.html#posts.page-section"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Papers"), href="index.html#papers.page-section"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Contact"), href="index.html#contact.page-section"), builder.CLASS("menu-item")),
        builder.CLASS("menu")
    )
    return menu






# <meta charset="utf-8">
# <title>Author Name</title>
# <meta name="viewport" content="width=device-width, initial-scale=1">
    
# <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js" async></script>
# <script type="text/x-mathjax-config">
#     MathJax.Hub.Config({
#         config: ["MMLorHTML.js"],
#         jax: ["input/TeX", "output/HTML-CSS", "output/NativeMML"],
#         extensions: ["MathMenu.js", "MathZoom.js"]
#     });
# </script>

# <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
# <script src="js/jquery.waypoints.min.js"></script>
# <script src="js/jquery.scrollTo.min.js"></script>


# <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css" integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf" crossorigin="anonymous">




index = builder.HTML(
    builder.HEAD(
            *make_head()
        ),
    builder.BODY(make_menu())
    )

print(html.etree.tostring(index, pretty_print=True).decode("utf-8"), file=open("huj.html", "w"))