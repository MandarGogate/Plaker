import os

from flask import render_template, Flask, jsonify
from flask_wtf import FlaskForm
from wtforms import TextAreaField

from placker import Placker

app = Flask(__name__)
app.secret_key = '64ee725abbb7eaa2082ec0ef6d129eb21cbeb27a9ca9bf9f01bbf6fdb0b9ad99651421e1206d78d8562528c46fa2171baed22e10ae99067f331f1cb1bc5d398a'


class PlakerForm(FlaskForm):
    maindoc = TextAreaField('maindoc')
    subdoc = TextAreaField('subdoc')


@app.route('/')
def home():
    form = PlakerForm()
    return render_template('index.html', form=form, data={"name": ""})


@app.route('/analyse/', methods=['post'])
def analyse():
    form = PlakerForm()
    if form.validate_on_submit():
        checker = Placker(form.maindoc.data.replace("\n"," \nNEWLINE "), form.subdoc.data.replace("\n"," \nNEWLINE "), min_len=3, check_synonyms=False)
        highlighted_text = checker.find_plagiarism().replace("NEWLINE", "\n</br>")
        return jsonify(data=highlighted_text)
    return jsonify(data=form.errors)


if __name__ == "__main__":
    app.run(host=os.getenv('IP', 'localhost'),
            port=int(os.getenv('PORT', 5000)), debug=False)
