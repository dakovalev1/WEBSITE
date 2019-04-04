import os
import shutil
import markdown
import configparser
import numpy
import lxml.html as html
import lxml.html.builder as builder
import dateparser
import sys


class Post:
    def __init__(self, id, text):
        md = markdown.Markdown(extensions=['mdx_math', 'meta'])
        self.id = id
        self.content = md.convert(text)
        self.title = md.Meta['title'][0]
        self.summary = markdown.markdown(md.Meta['summary'][0], extensions=['mdx_math'])
        self.date = dateparser.parse(md.Meta['date'][0])

class Paper:
    def __init__(self, id, text):
        md = markdown.Markdown(extensions=['meta'])
        md.convert(text)
        self.id = id
        self.title = md.Meta['title'][0]
        self.date = dateparser.parse(md.Meta['date'][0])
        self.authors = md.Meta['authors']
        


def load_posts():
    p_list = []
    for root, dirs, files in os.walk("posts"):
        for name in dirs:
            input = open(os.path.join(root, name, "index.md"), "r")
            p_list.append(Post(name, input.read()))
        break
    p_list.sort(key=lambda p: p.date, reverse=True)
    return p_list

def load_papers():
    p_list = []
    for root, dirs, files in os.walk("papers"):
        for name in dirs:
            input = open(os.path.join(root, name, "index.md"), "r")
            p_list.append(Paper(name, input.read()))
        break
    p_list.sort(key=lambda p: p.date, reverse=True)
    return p_list


def make_short_posts(p_list):
    tag_list = []
    for post in p_list:
        tag_list.append(builder.DIV(
            builder.H1(
                builder.A(post.title, href="posts/" + post.id + ".html"),
                builder.CLASS("post-title")
            ),
            html.fromstring(post.summary),
            builder.DIV(post.date.strftime("%d %b %Y, %H:%M"), builder.CLASS("post-date")),
            builder.CLASS("post-container")))
    return tag_list

def make_short_papers(p_list):
    tag_list = []
    for paper in p_list:
        
        authors = paper.authors[0]
        for a in paper.authors[1:-1]:
            authors += ", " + a
        if len(paper.authors) > 1:
            authors += " and " + paper.authors[-1]

        tag_list.append(builder.DIV(
            builder.H1(
                paper.title,
                builder.CLASS("paper-title")
            ),
            builder.DIV(html.fromstring(authors), builder.CLASS("paper-authors")),
            builder.DIV(paper.date.strftime("%d %b %Y"), builder.CLASS("paper-date")),
            builder.CLASS("paper-container")))
    return tag_list




def make_head():
    head = [
        #builder.BASE(href="https://dakovalev1.github.io/my_site/"),
        #builder.BASE(href="http://localhost/my_site/docs/"), # ONLY FOR DEBUG!!!
        builder.BASE(href=sys.argv[1]),
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
        #builder.SCRIPT("", src="js/jquery.waypoints.min.js"),
        #builder.SCRIPT("", src="js/jquery.scrollTo.min.js"),
        builder.LINK(rel="stylesheet",
            href="https://use.fontawesome.com/releases/v5.8.1/css/all.css",
            integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
            crossorigin="anonymous"),
        
        builder.LINK(rel="stylesheet",href="css/menu/menu.css"),
        builder.LINK(rel="stylesheet",href="css/common/common.css"),

        builder.SCRIPT("", src="js/menu.js"),
    ]

    return head
def make_menu():
    menu = builder.UL(
        builder.LI(builder.A(builder.I("", builder.CLASS("fas fa-bars")), href=""), builder.CLASS("menu-button")),
        builder.LI(builder.A(builder.B("Author Name"), href="index.html"), builder.CLASS("menu-title")),
        #builder.LI(builder.A(builder.B("Home"), href="index.html"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Posts"), href="posts.html"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Papers"), href="papers.html"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Contact"), href="contact.html"), builder.CLASS("menu-item")),
        builder.CLASS("menu")
    )
    return menu





def gen_index(p_list):
    index = builder.HTML(
        builder.HEAD(*make_head()),
        builder.BODY(make_menu(), builder.DIV("todo",builder.CLASS("section")))
    )

    print(html.etree.tostring(index, pretty_print=True).decode("utf-8"), file=open("docs/index.html", "w"))

def gen_posts(p_list):
    index = builder.HTML(
        builder.HEAD(*make_head()),
        builder.BODY(
            make_menu(),
            builder.DIV(
                builder.H1("Posts", builder.CLASS("section-title")),
                *make_short_posts(p_list),
                builder.CLASS("section")
            )
        )
    )
    print(html.etree.tostring(index, pretty_print=True).decode("utf-8"), file=open("docs/posts.html", "w"))

    for post in p_list:
        html_content = builder.DIV(
            builder.H1(post.title, builder.CLASS("full-post-title")),
            builder.DIV(post.date.strftime("%d %B %Y, %H:%M"), builder.CLASS("full-post-date")),
            builder.DIV(html.fromstring(post.content), builder.CLASS("full-post-content")),
            builder.CLASS("full-post-container")
        )

        page = builder.HTML(
            builder.HEAD(*make_head()),
            builder.BODY(make_menu(), html_content)
        )
        print(html.etree.tostring(page, pretty_print=True).decode("utf-8"), file=open("docs/posts/" + post.id + ".html", "w"))
    
def gen_papers(p_list):
    index = builder.HTML(
        builder.HEAD(*make_head()),
        builder.BODY(
            make_menu(),
            builder.DIV(
                builder.H1("Papers", builder.CLASS("section-title")),
                *make_short_papers(p_list),
                builder.CLASS("section")
            )
        )
    )
    print(html.etree.tostring(index, pretty_print=True).decode("utf-8"), file=open("docs/papers.html", "w"))

def gen_contact():
    index = builder.HTML(
        builder.HEAD(*make_head()),
        builder.BODY(make_menu(), builder.DIV("contact",builder.CLASS("section")))
    )
    print(html.etree.tostring(index, pretty_print=True).decode("utf-8"), file=open("docs/contact.html", "w"))

if len(sys.argv) != 2:
    print("usage: python main.py <baseurl>")
    exit(0)

if os.path.exists("docs"):
        shutil.rmtree("docs")

os.mkdir("docs")
os.mkdir("docs/posts")
shutil.copytree("src/css", "docs/css")
shutil.copytree("src/js", "docs/js")

post_list = load_posts()
paper_list = load_papers()

gen_index(post_list)
gen_posts(post_list)
gen_papers(paper_list)
gen_contact()




