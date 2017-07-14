from app import app
from flask import render_template, make_response, redirect, url_for, flash

app.secret_key = 'some_secret'

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

@app.route('/index/')
def validate_form():
    import xlrd
    workbook = xlrd.open_workbook('testing.xlsx')
    worksheet = workbook.sheet_by_index(0)

    # for T/F values: Enabled, RSTP and PoE
    for row in range(1, worksheet.nrows):
        # grab value for enable
        j = worksheet.cell_value(row, 5)
        # grab value for RSTP
        k = worksheet.cell_value(row, 6)
        # grab value for PoE
        m = worksheet.cell_value(row, 8)
        # print (j, k, m)
        if j == 1 or j == 0 or j == '':
            pass
        else:
            flash('Enabled must be either True or False')
            #break
        if k == 1 or k == 0 or k == '':
            pass
        else:
            flash('RSTP must be either True or False')
            #break
        if m == 1 or m == 0 or m == '':
            pass
        else:
            flash('PoE must be either True or False')
            #break

    # for checking that serial # is a 12 alpha numberic string
    #for row in range(1, worksheet.nrows):
        l = worksheet.cell(row, 1)
        # print(l.value.lower().replace('-',''))
        # print(len(l.value.lower().replace('-','')))
        if (len(l.value.lower().replace('-', '')) == 12):
            if l.ctype == 1 or l.ctype == 0:
                pass
            else:
                flash("Serial number must be a 12 character alpha numeric string")
                #break
        else:
            flash("Serial number must be a 12 character alpha numeric string")
            #break
    # print('Serial Number is done')

    # for checking that STP Guard must be 'disabled' 'root gound' or 'BPDU'
    #for row in range(1, worksheet.nrows):
        n = worksheet.cell(row, 7)
        # print(n.value.lower())
        if n.value.lower() == "disabled" or n.value.lower() == 'root guard' or n.value.lower() == 'bpdu guard' or n.value.lower() == '':
            pass
        else:
            flash("""STP Guard must be 'disabled' 'Root guard' or 'BPDU guard'""")
            #break
    # print('STP Guard is done')

    # for checking that Type is either access or trunk
    #for row in range(1, worksheet.nrows):
        o = worksheet.cell(row, 9)
        # print(o.value)
        if o.value == "trunk" or o.value == "access" or o.value == '':
            pass
        else:
            flash("Type must be either access or trunk")
            #break
    # print('Type is done')

    # VLAN must be a number
    #for row in range(1, worksheet.nrows):
        p = worksheet.cell(row, 10)
        # print(p.value)
        if p.ctype == 0 or p.ctype == 2:
            pass
        else:
            flash("VLAN must be a number")
            #break
    # print('VLAN is done')

    # Voice VLAN must be a number
    #for row in range(1, worksheet.nrows):
        q = worksheet.cell(row, 11)
        # print(q.value)
        if q.ctype == 0 or q.ctype == 2:
            pass
        else:

            flash("Voice VLAN must be a number")
            #break
    # print('Voice VLAN is done')

    # Port # must be a number
    #for row in range(1, worksheet.nrows):
        r = worksheet.cell(row, 2)
        # print(r.value)
        if r.ctype == 0 or r.ctype == 2:
            pass
        else:
            flash("Port # must be a number")
            #break
    # print('Port # is done')

    # Allowed VLANs can be all or comma seperated numbers
    #for row in range(1, worksheet.nrows):
        s = worksheet.cell(row, 12)
        # print(s.value)
        # print(s.ctype)
        if s.ctype == 0 or s.ctype == 1 and s.value == 'all' or s.ctype == 2 or s.value == '':
            pass
        else:
            flash("Allowed VLANs must be 'all' or numbers")
            #break
    # print('Allowed VLANs is done')

    return redirect(url_for('step2'))




if __name__ == "__main__":
    main()