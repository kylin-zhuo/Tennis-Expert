from flask import Flask, render_template, flash, redirect
from flask.ext.wtf import Form
# from flask.ext.bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from wtforms.validators import Required

from functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Set key'

class NameForm(Form):
    name = StringField('Player name', validators=[Required()])
    year = StringField('Year', validators=[Required()])
    submit = SubmitField('Submit')

def process(name, year):
    return str(name) + ', ' + str(year)

@app.route('/')
def index():
    # return 'INDEX'
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/facts', methods=['GET', 'POST'])
def facts():
    name = None
    year = None
    data = None
    nameForm = NameForm()

    if nameForm.validate_on_submit():
        name = nameForm.name.data
        year = nameForm.year.data
        nameForm.name.data = ''
        nameForm.year.data = ''
        flash('Player: ' + str(name))
        flash('Year: ' + str(year))
        data = player_info(name, year)

    return render_template('facts.html',
    name=name,
    year=year,
    form=nameForm,
    data=data)

@app.route('/head2head')
def head2head():
    return render_template('head2head.html')

if __name__ == '__main__':
    app.run(debug=True)
