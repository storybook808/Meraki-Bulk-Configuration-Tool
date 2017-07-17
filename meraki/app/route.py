from app import app
from flask import render_template, make_response, redirect, url_for, flash, request
import os
from werkzeug import secure_filename
import os, shutil
import openpyxl


app.secret_key = 'some_secret'

#route to file uploader
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    import os

    if request.method == 'POST':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'temp/')
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename)))
        path = os.path.abspath(os.path.join('app', 'temp'))
        current_file = os.listdir(path)
        print(current_file)
        if len(current_file) > 1:
            os.remove(os.path.join(path, current_file[1]))
            print("file removed brah")

        flash('file has been uploaded')

        return redirect(url_for('step2'))

#route to step1 page
@app.route('/')
@app.route('/step1.html')
def step1():
    return render_template('step1.html')

#route to step2 page
@app.route('/step2.html')
def step2():
    return render_template('step2.html')

#route to step3 page
@app.route('/step3.html')
def step3():
    return render_template('step3.html')

#route to validation script
@app.route('/index/')
def validate_form():
    import xlrd
    path = os.path.abspath(os.path.join('app', 'temp'))
    current_file = os.listdir(path)
    #open up working excel file to validate.
    workbook = xlrd.open_workbook(current_file[0])
    worksheet = workbook.sheet_by_index(0)

    flag = 0

    # for T/F values: Enabled, RSTP and PoE
    for row in range(1, worksheet.nrows):
        # grab value for enable
        j = worksheet.cell_value(row, 5)
        # grab value for RSTP
        k = worksheet.cell_value(row, 6)
        # grab value for PoE
        m = worksheet.cell_value(row, 8)
        if j == 1 or j == 0 or j == '':
            pass
        else:
            flash('ERROR! Enabled must be either True or False')
            flag += 1
        if k == 1 or k == 0 or k == '':
            pass
        else:
            flash('ERROR! RSTP must be either True or False')
            flag += 1
        if m == 1 or m == 0 or m == '':
            pass
        else:
            flash('ERROR! PoE must be either True or False')
            flag += 1

        #for checking that serial # is a 12 alpha numberic string
        # grab value for serial number
        l = worksheet.cell(row, 1)
        if (len(l.value.lower().replace('-', '')) == 12):
            if l.ctype == 1 or l.ctype == 0:
                pass
            else:
                flash("ERROR! Serial number must be a 12 character alpha numeric string")
                flag += 1
        else:
            flash("ERROR! Serial number must be a 12 character alpha numeric string")
            flag += 1

        # for checking that STP Guard must be 'disabled' 'root gound' or 'BPDU'
        # grab value for STP Guard
        n = worksheet.cell(row, 7)
        if n.value.lower() == "disabled" or n.value.lower() == 'root guard' or n.value.lower() == 'bpdu guard' or n.value.lower() == '':
            pass
        else:
            flash("""ERROR! STP Guard must be 'disabled' 'Root guard' or 'BPDU guard'""")
            flag += 1

        #for checking that Type is either access or trunk
        # grab value for type
        o = worksheet.cell(row, 9)
        if o.value == "trunk" or o.value == "access" or o.value == '':
            pass
        else:
            flash("ERROR! Type must be either access or trunk")
            flag += 1

        # for checking that VLAN is a number
        # grab value for VLAN
        p = worksheet.cell(row, 10)
        # print(p.value)
        if p.ctype == 0 or p.ctype == 2:
            pass
        else:
            flash("ERROR! VLAN must be a number")
            flag += 1

        #for checking that Voice VLAN must be a number
        # grab value for Voice VLAN
        q = worksheet.cell(row, 11)
        if q.ctype == 0 or q.ctype == 2:
            pass
        else:
            flash("ERROR! Voice VLAN must be a number")
            flag += 1


        #for checking that Port # must be a number
        # grab value for port #
        r = worksheet.cell(row, 2)
        if r.ctype == 0 or r.ctype == 2:
            pass
        else:
            flash("ERROR! Port # must be a number")
            flag += 1

        #for checking that Allowed VLANs can be all or comma seperated numbers
        # grab value for allowed VLANS
        s = worksheet.cell(row, 12)
        if s.ctype == 0 or s.ctype == 1 and s.value == 'all' or s.ctype == 2 or s.value == '':
            pass
        else:
            flash("ERROR! Allowed VLANs must be 'all' or numbers")
            flag += 1

    # if no error messages then display validation complete
    if flag == 0:
        flash('Validation Complete')

    # return same template page to display messages
    return redirect(url_for('step2'))


@app.route('/main', methods=['POST'])
def main():
    import merakiapi
    import shutil

    class Device:
        def __init__(self, row):
            self.hostname = row[0]
            self.serial_number = row[1]
            self.ip = row[2]
            self.vlan = row[3]
            self.subnet_mask = row[4]
            self.primary_dns = row[5]
            self.secondary_dns = row[6]
            self.tags = row[7]

    class SwitchPort:
        def __init__(self, row):
            self.hostname = row[0]
            self.serial_number = row[1]
            self.port_number = row[2]
            self.name = row[3]
            self.tags = row[4]

            if row[5] == "TRUE":
                self.enabled = True
            else:
                self.enabled = False

            if row[6] == "TRUE":
                self.rstp = True
            else:
                self.rstp = False

            self.stp_guard = row[7]

            if row[8] == "TRUE":
                self.poe = True
            else:
                self.poe = False

            self.type = row[9]
            self.vlan = row[10]
            self.voice_vlan = row[11]
            self.allowed_vlan = row[12]

    def time():
        import time

        date = time.strftime("%d/%m/%Y")
        time = time.strftime("%H:%M:%S")

        return date + "_" + time

    def sessionID():
        import string
        import random

        chars = string.ascii_uppercase
        size = 10

        return ''.join(random.choice(chars) for _ in range(size))

    def file_rename():

        path = os.path.abspath(os.path.join('app', 'temp'))
        current_file = os.listdir(path)
        print("file_RE_NAME")
        print(current_file)
        print(os.path.abspath(os.path.join('temp', current_file[0])))
        rename_src_path = os.path.abspath(os.path.join("app","temp", current_file[0]))
        rename_dst_path = os.path.abspath(
            os.path.join('app', 'temp', current_file[0].replace(".xslx", "") + "_" + sessionID() + "_" + time() + ".xslx"))
        new_name = shutil.move(rename_src_path, rename_dst_path)
        print(new_name)
        return None

    # def main():
    #     # Pull the configurations.
    #     configurations = {}
    #     file_1 = open("Device Base Configuration.csv")
    #     csv_1 = csv.reader(file_1)
    #     for row in csv_1:
    #         configurations[row[0]] = Device(row)
    #
    #     # API key.
    #     api_key = ""
    #
    #     # Get the organization name.
    #     print("Organization Name:")
    #     org_name = raw_input()
    #
    #     # Pull the organizations associated to the provided API key.
    #     orgs = merakiapi.myorgaccess(api_key, True)
    #
    #     # Look for the organization that we want to configure.
    #     org_id = ""
    #     for org in orgs:
    #         if org_name in org["name"]:
    #             org_id = org["id"]
    #
    #     if org_id == "":
    #         print("Organization not found.")
    #         return
    #
    #     # Pull the networks associated with the organization.
    #     networks = merakiapi.getnetworklist(api_key, org_id, True)
    #
    #     # Pull the devices from all of the networks.
    #     devices = []
    #     for network in networks:
    #         devices += merakiapi.getnetworkdevices(api_key, network["id"], True)
    #
    #     # Apply configuration to the devices and push them to Meraki.
    #     for device in devices:
    #         device["name"] = configurations[device["serial"]].hostname
    #         merakiapi.updatedevice(api_key, device["networkId"], device["serial"], device["name"], "", "", "", "", True)
    #
    #     return

    #file_rename()
    ### Find file path to pull configurations ###
    path = os.path.abspath(os.path.join('app', 'temp'))
    # path = os.path.join(initial_path, 'temp')
    current_file = os.listdir(path)
    # print(initial_path)
    # print(path)
    # print(current_file)
    print(current_file[0])
    print(os.path.join(path, current_file[0]))
    temp_path = os.path.join(path, current_file[0])  # path of configuration file

    ### Pull the configurations. ###
    configurations = {}
    from openpyxl import load_workbook
    wb = load_workbook(filename=temp_path)
    first_sheet = wb.get_sheet_names()[0]
    ws = wb[first_sheet]

    ### valid row count ###
    valid_row = 0  # will be incremented to the number of valid rows
    threshold = 2  # how many consecutive blank rows are allow before program stops scanning excel content
    real_row = 0  # track the actual row in excel file, including blank rows
    th_count = threshold
    while (th_count != 0):
        real_row += 1
        if (ws.cell(row=real_row, column=2).value != None and ws.cell(row=real_row, column=3).value != None):
            # print(ws.cell(row = valid_row + 1, column=2).value)
            valid_row += 1
            th_count = threshold  # if blank row is not consecutive to the number of threshold, reset th_count
        elif (ws.cell(row=real_row, column=2).value == None and ws.cell(row=real_row, column=3).value != None):
            print("row", real_row, "has incomplete entry")
        elif (ws.cell(row=real_row, column=2).value != None and ws.cell(row=real_row, column=3).value == None):
            print("row", real_row, "has incomplete entry")
        else:
            th_count -= 1

    progress_total = valid_row - 1  # save total number of excel entries to track for progress while compiling
    progress_count = 0  # initialize variable for progress count

    ### create dictionary for switch port ###
    my_row = []
    i = 0
    while (valid_row != 0):
        i += 1
        if (ws.cell(row=i, column=2).value == None and ws.cell(row=i, column=3).value != None):
            pass
        elif (ws.cell(row=i, column=2).value != None and ws.cell(row=i, column=3).value == None):
            pass
        elif (ws.cell(row=i, column=2).value == None and ws.cell(row=i, column=3).value == None):
            pass
        else:
            for j in range(1, 14):  # max column number
                my_row.append(ws.cell(row=i, column=j).value)
            configurations[ws.cell(row=i, column=2).value, str(ws.cell(row=i, column=3).value)] = SwitchPort(
                my_row)  # dictionary
            # print(ws.cell(row = i, column = 2).value , str(ws.cell(row = i, column=3).value))
            # print(my_row)
            my_row = []  # reset
            valid_row -= 1

    # print(configurations)

    # API key.
    api_key = "8b43aaa7b92b6d3ad06234e6f581077620d3e512"

    # Get the organization name.
    print("Organization Name:")
    org_name = input()

    # Pull the organizations associated to the provided API key.
    orgs = merakiapi.myorgaccess(api_key, True)

    # Look for the organization that we want to configure.
    org_id = ""
    for org in orgs:
        if org_name in org["name"]:
            org_id = org["id"]

    if org_id == "":
        print("Organization not found.")

    ### Pull the networks associated with the organization. ###
    networks = merakiapi.getnetworklist(api_key, org_id, True)

    ### Pull the devices from all of the networks. ###
    devices = []
    for network in networks:
        devices += merakiapi.getnetworkdevices(api_key, network["id"], True)
    # print devices

    switch_ports = []
    for device in devices:
        current_switch_ports = []
        if device["model"].startswith("MS"):
            # current_switch_port = merakiapi.getswitchports(api_key, device["serial"])
            # current_switch_port["serial"] = device["serial"]
            current_switch_ports = merakiapi.getswitchports(api_key, device["serial"], True)

        # Label all current switch ports with the serial number of the parent switch.
        for switch_port in current_switch_ports:
            switch_port["serial"] = device["serial"]

        # Append the switch ports for the current switch to the master list.
        switch_ports += current_switch_ports

    print(switch_ports)

    ### Apply configuration to the devices and push them to Meraki. ###
    for switch_port in switch_ports:
        try:
            switch_port["name"] = configurations[switch_port["serial"], str(switch_port["number"])].name
        except:
            continue
        switch_port["tags"] = configurations[switch_port["serial"], str(switch_port["number"])].tags
        switch_port["enabled"] = configurations[switch_port["serial"], str(switch_port["number"])].enabled
        switch_port["rstpEnabled"] = configurations[switch_port["serial"], str(switch_port["number"])].rstp
        switch_port["stpGuard"] = configurations[switch_port["serial"], str(switch_port["number"])].stp_guard
        switch_port["poeEnabled"] = configurations[switch_port["serial"], str(switch_port["number"])].poe
        switch_port["type"] = configurations[switch_port["serial"], str(switch_port["number"])].type
        switch_port["vlan"] = configurations[switch_port["serial"], str(switch_port["number"])].vlan
        switch_port["voiceVlan"] = configurations[switch_port["serial"], str(switch_port["number"])].voice_vlan
        switch_port["allowedVlans"] = configurations[switch_port["serial"], str(switch_port["number"])].allowed_vlan

        # print (switch_port["enabled"])


        merakiapi.updateswitchport(api_key, switch_port["serial"], switch_port["number"], switch_port["name"],
                                   switch_port["tags"], switch_port["enabled"], switch_port["type"],
                                   switch_port["vlan"], switch_port["voiceVlan"], switch_port["allowedVlans"],
                                   switch_port["poeEnabled"], "", switch_port["rstpEnabled"], switch_port["stpGuard"],
                                   "")
        progress_count += 1
        progress_percent = '{:.1%}'.format(progress_count / progress_total)
        print(progress_percent)

    archive_path = os.path.abspath(os.path.join('app', 'archive'))
    shutil.copy(temp_path, archive_path)

    return "IT WORKS!"


if __name__ == "__main__":
    main()
