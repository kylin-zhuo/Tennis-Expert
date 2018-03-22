from flask import Flask, render_template, flash, redirect
from flask.ext.wtf import Form
# from flask.ext.bootstrap import Bootstrap
from wtforms import StringField, SubmitField, validators
from wtforms.validators import Required

from functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Set key'

class NameForm(Form):
    name = StringField('Player name', validators=[Required()])
    year = StringField('Year', validators=[Required()])
    submit = SubmitField('Submit')

class RivaryForm(Form):
    name1 = StringField('Player 1', validators=[Required()])
    name2 = StringField('Player 2', validators=[Required()])
    from_year = StringField('From', validators=[validators.Length(min=0, max=4)])
    to_year = StringField('To', validators=[validators.Length(min=0, max=4)])
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
    keys = None
    nameForm = NameForm()

    if nameForm.validate_on_submit():
        name = nameForm.name.data
        year = nameForm.year.data
        nameForm.name.data = ''
        nameForm.year.data = ''
        flash('Player: ' + str(name))
        flash('Year: ' + str(year))
        keys, data = player_info(name, year)

    return render_template('facts.html',
    name=name,
    year=year,
    form=nameForm,
    keys=keys,
    data=data)

@app.route('/head2head', methods=['GET', 'POST'])
def head2head():
    name1, name2 = None, None
    from_year, to_year = None, None
    result = None
    rivaryForm = RivaryForm()

    if rivaryForm.validate_on_submit():
        name1 = rivaryForm.name1.data
        name2 = rivaryForm.name2.data
        from_year = rivaryForm.from_year.data
        to_year = rivaryForm.to_year.data
        # rivaryForm.name1.data = ''
        # rivaryForm.name2.data = ''
        flash('Player1: ' + str(name1))
        flash('Player2: ' + str(name2))
        result = rivary(name1, name2, from_year, to_year)

    return render_template('head2head.html', result=result, form=rivaryForm)

if __name__ == '__main__':
    app.run(debug=True)
