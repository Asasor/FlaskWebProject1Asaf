"""
Routes and views for the flask application.
"""

from datetime import datetime
import numpy as np
from flask   import Flask, render_template, flash, request
from FlaskWebProject1Asaf import app
from FlaskWebProject1Asaf.Models.QueryFormStructure import QueryFormStructure 
from FlaskWebProject1Asaf.Models.QueryFormStructure import LoginFormStructure 
from FlaskWebProject1Asaf.Models.QueryFormStructure import UserRegistrationFormStructure
from FlaskWebProject1Asaf.Models.ScoutingDataStructure import create_DataSheetsServiceRoutines
from FlaskWebProject1Asaf.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
import matplotlib.pyplot as plt
from wtforms import ValidationError
import pandas as pd
from datetime import datetime
import base64
import io
from os import path
import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


db_Functions = create_LocalDatabaseServiceRoutines() 
sd_Functions = create_DataSheetsServiceRoutines()

def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

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
        message='Photos of various things in the FIRST FRC program'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='About the frc scouting data analyzer.'
    )
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)

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
    plt.rcParams.update({'font.size': 50})
    Ranking = ''
    Team_Number = ''
    df = sd_Functions.ReadCSVSheetsDB('1E9-iezDKAkKzp7WB_2_je4W7uCPko-7V4GpmpaAV4f4', 0)
    df = df.set_index('Team Number')
    avgRanking = sum(df['Ranking Score'].tolist()) / len(df['Ranking Score'].tolist())
    highestRanking = max(df['Ranking Score'].tolist())
    subtitle = 'table is'
    plt.rcParams.update({'font.size': 75})
    fig2 = plt.figure(figsize=(100,30))
    ax1, ax2 = fig2.subplots(1,2)
    raw_data_table = df.to_html(classes = 'table table-hover')

    form = QueryFormStructure(request.form)
     
    if (request.method == 'POST' ):
        name = form.name.data
        Ranking = name
        if (int(name) in df.index):
            Team_Number = df.loc[int(name),'Ranking Score']
            
            raw_data_table = ""
            subtitle = 'For comparison, The average ranking is - ' + str(avgRanking) + ' and the highest ranking score is - ' + str(highestRanking) + '.'
            ax1.pie([df.loc[int(name),'Ranking Score'],highestRanking - df.loc[int(name),'Ranking Score']], labels = ["team ranking score \n blue", "the difference between \n the largest ranking \n score and the \n team's ranking score \n orange"])
            ax2.bar(x =  list(df.columns)[1:-1], height = list(df.loc[int(name)])[1:-1])
        else:
            Team_Number = name + ', no such team'
        form.name.data = ''
    chart2 = plot_to_img(fig2)


    return render_template('Query.html', 
            form = form, 
            name = Team_Number, 
            Ranking = Ranking,
            raw_data_table = raw_data_table,
            title='Query by the user',
            year=datetime.now().year,
            message='This page will use the web forms to get user input',
            lower_heading=subtitle,
            chart2 = chart2,
            height2 = '500',
            width2 = '1000'
        )   
@app.route('/datamodel', methods=['GET', 'POST'])
def datamodel():
    """Renders the data model page."""
 
    return render_template(
        'datamodel.html',
        title='This is my Data Model page abou FRC scouting',
        year=datetime.now().year,
        message='In this page some datasets that present data on the distribution of points in FIRST competitions are presented',
    )
@app.route('/dataset1')
def DataSet1():

    df = sd_Functions.ReadCSVSheetsDB('1zGAOSxSsuSd9UdknH-TBqRQ11VsUON6qQPu2dPtY3GE', 0)
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'dataset1.html',
        title='This is the sheets data page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the google sheets scouting points data by the given link'
    )
@app.route('/dataset2')
def DataSet2():

    df = sd_Functions.ReadCSVSheetsDB('1E9-iezDKAkKzp7WB_2_je4W7uCPko-7V4GpmpaAV4f4', 0)
    raw_data_table = df.to_html(classes = 'table table-hover')


    """Renders the contact page."""
    return render_template(
        'dataset2.html',
        title='This is the blue alliance page',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='In this page we will display the team overview sheet'
    )