import os
import shutil
import markdown
import configparser
import numpy
import lxml.html as html
import lxml.html.builder as builder
import dateparser
import sys
import json

base_url = ""

base_path = "/Users/kovaled/Documents/dakovalev1.github.io"


class Post:
    def __init__(self, id, text):
        md = markdown.Markdown(extensions=['mdx_math', 'meta', 'extra'])
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
        self.links = json.loads(md.Meta['links'][0])
        
        


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
                builder.A(post.title, href=base_url + "posts/" + post.id),
                builder.CLASS("post-title")
            ),
            html.fromstring(post.summary),
            builder.DIV(post.date.strftime("%d %b. %Y, %H:%M"), builder.CLASS("post-date")),
            builder.CLASS("post-container")))
    return tag_list

def make_short_papers(p_list, count=None):
    authors_dict = json.load(open("authors.json"))

    def gen_author_link(a):
        if a in authors_dict:
            return "<a href=\"" + authors_dict[a] + "\">" + a + "</a>"
        else:
            return a

    tag_list = []
    for paper in p_list[:count]:
        
        authors = gen_author_link(paper.authors[0])
        for a in paper.authors[1:-1]:
            authors += ", " + gen_author_link(a)
        if len(paper.authors) > 1:
            authors += " and " + gen_author_link(paper.authors[-1])

        links = []

        for key in paper.links:
            links += [builder.A(key, href=paper.links[key])]

        tag_list.append(builder.DIV(
            builder.H1(
                paper.title,
                builder.CLASS("paper-title")
            ),
            builder.DIV(html.fromstring(authors), builder.CLASS("paper-authors")),
            builder.DIV(paper.date.strftime("%d %b. %Y"), builder.CLASS("paper-date")),
            builder.DIV(*links, builder.CLASS("paper-links")),
            builder.CLASS("paper-container")))
    return tag_list




def make_head():
    head = [
        #builder.BASE(href="https://dakovalev1.github.io/my_site/"),
        #builder.BASE(href="http://localhost/my_site/docs/"), # ONLY FOR DEBUG!!!
        #builder.BASE(href=sys.argv[1]),
        builder.META(charset="utf-8"),
        builder.TITLE("Dmitry Kovalev"),
        builder.META(name="viewport", content = "width=device-width, initial-scale=1"),
        builder.SCRIPT("", type="text/javascript", src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js",async="async"),
        builder.SCRIPT(open("src/js/mathjax.js").read(),
            type="text/x-mathjax-config"),
        builder.SCRIPT("", src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"),
        #builder.SCRIPT("", src="js/jquery.waypoints.min.js"),
        #builder.SCRIPT("", src="js/jquery.scrollTo.min.js"),
        builder.LINK(rel="stylesheet",
            href="https://use.fontawesome.com/releases/v5.8.1/css/all.css",
            integrity="sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf",
            crossorigin="anonymous"),
        builder.LINK(rel="stylesheet",
            href="https://cdn.rawgit.com/jpswalsh/academicons/master/css/academicons.min.css"),

        builder.LINK(rel="stylesheet",href=base_url + "css/menu.css"),
        builder.LINK(rel="stylesheet",href=base_url + "css/common.css"),

        builder.SCRIPT("", src=base_url + "js/menu.js"),
        builder.SCRIPT("", src=base_url + "js/scroll.js"),
        
    ]

    return head
def make_menu(index = False):

    if index:
        contact = builder.A(builder.B("Contact"), builder.CLASS("hashtag"), href="#contact")
    else:
        contact = builder.A(builder.B("Contact"), href=base_url+"#contact")


    menu = builder.UL(
        builder.LI(builder.A(builder.I("", builder.CLASS("fas fa-bars")), href=""), builder.CLASS("menu-button")),
        builder.LI(builder.A(builder.B("Dmitry Kovalev"), href=base_url), builder.CLASS("menu-title")),
        builder.LI(builder.A(builder.B("Posts"), href=base_url+"posts.html"), builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("Papers"), href=base_url+"papers.html"), builder.CLASS("menu-item")),
        builder.LI(contact, builder.CLASS("menu-item")),
        builder.LI(builder.A(builder.B("CV"), href=base_url+"CV/cv.pdf"), builder.CLASS("menu-item")),
        builder.CLASS("menu")
    )
    return builder.DIV(menu, builder.CLASS("menu-container"))





def gen_index(p_list):

    about = html.fromstring(open("src/html/about.html").read())
    contact = html.fromstring(open("src/html/contact.html").read())

    index = builder.HTML(
        builder.HEAD(*make_head(), builder.LINK(rel="stylesheet",href=base_url + "css/about.css")),
        builder.BODY(
            make_menu(index=True),
            about,
            contact
        )
    )


    print(html.etree.tostring(index, pretty_print=True, method='html').decode("utf-8"), file=open(os.path.join(base_path, "index.html"), "w"))

def gen_posts(p_list):
    index = builder.HTML(
        builder.HEAD(*make_head()),
        builder.BODY(
            make_menu(),
            builder.DIV(
                builder.H1("Posts", builder.CLASS("section-title")),
                *make_short_posts(p_list),
                builder.CLASS("section")
            ),
            style="background-color:#f7f7f7"
        )
    )
    print(html.etree.tostring(index, pretty_print=True, method='html').decode("utf-8"), file=open(os.path.join(base_path, "posts.html"), "w"))

    for post in p_list:
        html_content = builder.DIV(
            builder.H1(post.title, builder.CLASS("full-post-title")),
            builder.DIV(post.date.strftime("%d %B %Y, %H:%M"), builder.CLASS("full-post-date")),
            builder.DIV(html.fromstring(post.content), builder.CLASS("full-post-content")),
            builder.CLASS("full-post-container")
        )

        page = builder.HTML(
            builder.HEAD(*make_head(), builder.SCRIPT("", src=base_url + "js/table.js"),),
            builder.BODY(make_menu(), html_content)
        )
        print(html.etree.tostring(page, pretty_print=True, method='html').decode("utf-8"), file=open(os.path.join(base_path, "posts", post.id, "index.html"), "w"))
    
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
    print(html.etree.tostring(index, pretty_print=True, method='html').decode("utf-8"), file=open(os.path.join(base_path, "papers.html"), "w"))

if len(sys.argv) != 2:
    print("usage: python main.py <baseurl>")
    exit(0)
else:
    base_url = sys.argv[1]

def del_path(path):
    if os.path.exists(os.path.join(base_path, path)):
        shutil.rmtree(os.path.join(base_path, path))

def del_file(path):
    if os.path.exists(os.path.join(base_path, path)):
        os.remove(os.path.join(base_path, path))


del_path("posts")
del_path("css")
del_path("js")
del_path("res")

del_file("index.html")
del_file("posts.html")
del_file("papers.html")


if not os.path.exists(base_path):
    os.mkdir(base_path)

shutil.copytree("posts", os.path.join(base_path, "posts"))
shutil.copytree("src/css", os.path.join(base_path, "css"))
shutil.copytree("src/js", os.path.join(base_path, "js"))
shutil.copytree("res", os.path.join(base_path, "res"))

post_list = load_posts()
paper_list = load_papers()

gen_index(paper_list)
gen_posts(post_list)
gen_papers(paper_list)




