from flask import Flask, render_template, request
from config import Config
from forms import LoginForm
from search import search
app = Flask(__name__)
app.config.from_object(Config)
@app.route('/index')
def index():
    form = LoginForm()
    return render_template('index.html', form=form)

@app.route('/searchText', methods = ['POST'])
def searchText():
    searchtext = request.form['searchtext']
    return search(searchtext)