from app import app
from flask import render_template, request, redirect, url_for
import os
from werkzeug import secure_filename

#@app.route('/upload')
#def upload_file2():
#    return render_template('upload.html')



@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'temp/')
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename)))
        return 'FILE UPLOADED'

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

''''@app.route('/csv/')
def download_csv():
    csv = 'Hostname,Serial Number,Port Number,Name,Tags,Enabled,RSTP,STP Guard,PoE,Type,VLAN,Voice VLAN,Allowed VLANs'
    response = make_response(csv)
    cd = 'attachment; filename=template.csv'
    response.headers['Content-Disposition'] = cd
    response.mimetype = 'text/csv'

    return response
'''
