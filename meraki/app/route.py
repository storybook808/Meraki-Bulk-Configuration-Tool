from app import app
from flask import Response, render_template, session, redirect, url_for, flash, request
import os
from werkzeug import secure_filename
import os, shutil
app.secret_key = 'some_secret'

from flask import Response
import time
from app import app

# route to file uploader


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    import os

    if request.method == 'POST':

        # Get the absolute path of the added file
        path = os.path.abspath(os.path.join('app', 'temp'))
        current_file = os.listdir(path)
        if len(current_file) > 0:
            # remove all files except the first
            os.remove(os.path.join(path, current_file[0]))
            print("file removed")

        # Obtain the absolute path to the file to upload using os module
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Save the uploaded file into the path specified
        # This path saves it into the current directory, then uses the join method
        # To put the file into the temp folder
        app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'temp/')
        f = request.files['file']

        # Save the file in temp
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename)))

        # Debug print, current_file should list all files within the temp folder
        print(current_file)

        # if there is more than a single file in the temp folder remove the extra files

        if len(current_file) > 1:
            # remove all files except the first
            os.remove(os.path.join(path, current_file[1]))
            print("file removed")

        flash('File has been uploaded')


        return redirect(url_for('step2'))



@app.route('/')

@app.route('/step1.html')
def step1():
    return render_template('step1.html')

# Route to step2 page
# Formats the step2.html page
@app.route('/step2.html')
def step2():
    return render_template('step2.html')

# Route to step2 page
# Formats the step2.html page
@app.route('/step2a.html')
def step2a():
    return render_template('step2a.html')


# Route to step3 page
# Formats the step1.html page
@app.route('/step3.html')
def step3():
    return render_template('step3.html')


