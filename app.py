from flask import Flask, flash, redirect, render_template, request, session, url_for, make_response
from cs50 import get_string
from bs4 import BeautifulSoup
from requests import get
# Configure application
app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index(name=""):
#   q = get_string("Which Wikipedia article? ")
    q = "Computer Science"
    q = request.args.get('name', name)
    if request.method == "POST":
        q = request.form.get("testField")
        print(q)
    url_q = add_underscores(q) 

    # get wikipedia page
    page = get("https://en.wikipedia.org/wiki/" + url_q)

    # parse html
    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find('h1', id='firstHeading').get_text()
    
    # get image in table
    img = soup.find('table').find('img').get('src')
    if not img:
        img = "No available image"

    
    body = soup.find('div', class_='mw-parser-output')
    if not body:
        print("No Wikipedia page available for " + q)
        return render_template("index.html", title=title, final_text="No Wikipedia page available for " + q, img=img)
    footer = soup.find('li', id='footer-info-lastmod').get_text()

    if not footer: 
        footer = "No footer available"
        return render_template("index.html", title=title, final_text="No Wikipedia page available for " + q, img=img)
    

    # get first 5 p tags in body
    body_text = body.find_all('p', limit=5)

    print("Title: " + title)
    print("Description: " + first_sentence(body_text, q.split(" ")[0]))
    print("Img URL: " + img[2:len(img)])
    print("Footer: " + footer)

    

    return render_template("index.html", title=title, final_text=first_sentence(body_text, q.split(" ")[0]), img = img[2:len(img)], footer=footer)
# return the first sentence containing a keyword in a block of tags

@app.route('/<string:query>')
def hello(query):
    return 'welcome %s' % query

@app.route('/result', methods=["GET", "POST"])
def query():
    if request.method == "POST":
        query_keyword = request.form.get("wikipedia")
        return redirect(url_for('hello', query=query_keyword))
    else:
        return render_template("result.html")


def first_sentence(b, q):
    # for each tag in a block of tags
    for p in b:
        sentences = p.get_text().split(".")
        # for each sentence of text in a tag
        for s in sentences:
            if q.lower() in s.lower():
                return s
    return b[0].get_text().split(".")[0]

def add_underscores(s):
    return s.replace(" ", "_")
