from flask import Flask, render_template, flash, redirect
from flask.ext.wtf import Form
# from flask.ext.bootstrap import Bootstrap
from wtforms import StringField, SubmitField, BooleanField, validators
from wtforms.validators import Required

from functions import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Set key'

class NameForm(Form):
    name = StringField('Player name', validators=[Required()])
    year = StringField('Year', validators=[validators.Length(min=0, max=4)])
    davis_cup = BooleanField('Include Davis Cup?', default="checked")
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
    davis_cup = False
    nameForm = NameForm()

    if nameForm.validate_on_submit():
        name = nameForm.name.data
        year = nameForm.year.data
        davis_cup = nameForm.davis_cup.data
        nameForm.name.data = ''
        nameForm.year.data = ''
        flash('Player: ' + str(name))
        flash('Year: ' + str(year))
        keys, data = player_info(name, year, davis_cup)

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
    chart = None
    series = None
    title = None
    xAxis = None
    yAxis = None

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

        ## the following is for testing
        chart = {"renderTo": 'chartID', "type": 'bar', "height": 450,}
        series = [
        {"name": name1, "data": [result['h2h'][0], result['h2h_grass'][0], result['h2h_hard'][0], result['h2h_clay'][0]]}, 
        {"name": name2, "data": [result['h2h'][1], result['h2h_grass'][1], result['h2h_hard'][1], result['h2h_clay'][1]]}]
        title = {"text": 'Head-to-head between ' + name1 + ' and ' + name2}
        xAxis = {"categories": ['All', 'Grass', 'Hard', 'Clay']}
        yAxis = {"title": {"text": 'Wins'}}

    return render_template('head2head.html', result=result, form=rivaryForm, 
         chartID='chartID', chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

if __name__ == '__main__':
    app.run(debug=True)
