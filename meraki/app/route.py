from app import app
from flask import render_template

app.secret_key = 'some_secret'


# route to file uploader
# Route to step1 page
# Formats the step1.html page


@app.route('/')
@app.route('/step1.html')
def step1():
    return render_template('step1.html')


# Route to step2 page
# Formats the step2.html page
@app.route('/step2.html')
def step2():
    return render_template('step2.html')


# Route to step3 page
# Formats the step1.html page
@app.route('/step3.html')
def step3():
    return render_template('step3.html')


