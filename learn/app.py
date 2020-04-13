

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from forms import ContactForm
app = Flask(__name__)
app.config['SECRET_KEY'] = b'secret'
@app.route('/',methods=['GET','POST'])
def hello():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for("success"))
    return render_template("index.html", title="Index Page", description = "This is Index",form = form)

@app.route('/successful')
def success():
    return "SUCCESS"