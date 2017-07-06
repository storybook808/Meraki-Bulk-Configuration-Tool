#!/usr/bin/python3

#imports file path of file you need

#this opens up a window to choose a file

#from tkinter import *
import os
from flask import render_template
#from tkinter.filedialog import askopenfilename

from app import app

@app.route('/step2')
def step2():
    return render_template('step2.html')

@app.route('/file')
def file(file):
    filename = askopenfilename()
    flash('opening file')



