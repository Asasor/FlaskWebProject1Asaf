"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask   import Flask, render_template, flash, request
from FlaskWebProject1Asaf import app
from FlaskWebProject1Asaf.Models.QueryFormStructure import QueryFormStructure 
from FlaskWebProject1Asaf.Models.QueryFormStructure import LoginFormStructure 
from FlaskWebProject1Asaf.Models.QueryFormStructure import UserRegistrationFormStructure 
from FlaskWebProject1Asaf.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError
import pandas as pd
from datetime import datetime
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Frc Scouting Analyzer contact info (built by Asaf Soreq).'
    )

@app.route('/photoalbum')
def photoalbum():
    """Renders the contact page."""
    return render_template(
        'photoalbum.html',
        title='Photo Album',
        year=datetime.now().year,
        message='Photos of ducks of all shapes and sizes'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/Query', methods=['GET', 'POST'])
def Query():

    Name = None
    Country = ''
    capital = ''
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'static\\Data\\capitals.csv'))
    df = df.set_index('Country')

    raw_data_table = df.to_html(classes = 'table table-hover')

    form = QueryFormStructure(request.form)
     
    if (request.method == 'POST' ):
        name = form.name.data
        Country = name
        if (name in df.index):
            capital = df.loc[name,'Capital']
            raw_data_table = ""
        else:
            capital = name + ', no such country'
        form.name.data = ''



    return render_template('Query.html', 
            form = form, 
            name = capital, 
            Country = Country,
            raw_data_table = raw_data_table,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input'
        )
@app.route('/datamodel', methods=['GET', 'POST'])
def datamodel():
    """Renders the contact page."""
    return render_template(
        'datamodel.html',
        title='This is my Data Model page abou UFO',
        year=datetime.now().year,
        message='In this page we will display the datasets we are going to use in order to answer ARE THERE UFOs'
    )