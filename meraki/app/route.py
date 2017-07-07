from app import app
from flask import render_template, make_response

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
