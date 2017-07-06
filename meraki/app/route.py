from app import app
from flask import render_template

@app.route('/')

@app.route('/step1.html')
def step1():
    return render_template('step1.html')

@app.route('/step2.html')
def step2():
    return render_template('step2.html')

@app.route('/step3.html')
def step3():
    return render_template('step3.html')

#comment