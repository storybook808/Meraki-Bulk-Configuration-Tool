from app import app
from flask import render_template, make_response, redirect, url_for, flash
import os
from werkzeug import secure_filename


app.secret_key = 'some_secret'

#route to file uploader
@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        app.config['UPLOAD_FOLDER'] = os.path.join(current_dir, 'temp/')
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'],
                            secure_filename(f.filename)))
        return 'FILE UPLOADED'

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
    #open up working excel file to validate.
    workbook = xlrd.open_workbook('testing.xlsx')
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
                #break
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
    import csv
    import merakiapi
    import os
    import random

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

            if row[5].lower() == "true":
                self.enabled = True
            else:
                self.enabled = False

            if row[6].lower() == "true":
                self.rstp = True
            else:
                self.rstp = False

            self.stp_guard = row[7]

            if row[8].lower() == "true":
                self.poe = True
            else:
                self.poe = False

            self.type = row[9]
            self.vlan = row[10]
            print(row)
            self.voice_vlan = row[11]
            self.allowed_vlan = row[12]

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

        # Pull the configurations.
    random.seed()
    configurations = {}
    path = os.path.abspath(os.path.join('app', 'temp'))
    #path = os.path.join(initial_path, 'temp')

    current_file = os.listdir(path)
   # print(initial_path)
    print(path)
    print(current_file)
    print(current_file[0])
    print(os.path.join(path,current_file[0]))
    temp_path = os.path.join(path,current_file[0])
    file_1 = open(temp_path)
    csv_1 = csv.reader(file_1)
    for row in csv_1:
        configurations[row[1] + str(row[2])] = SwitchPort(row)

    print(configurations)

    # API key.
    api_key = "36b0616a7dda8c0017f621cb66a4e666effad0d0"

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

####
    # Pull the networks associated with the organization.
    networks = merakiapi.getnetworklist(api_key, org_id, True)

    # Pull the devices from all of the networks.
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

    # Apply configuration to the devices and push them to Meraki.
    for switch_port in switch_ports:
        print("ENTER4")
        try:
            switch_port["name"] = configurations[switch_port["serial"] + str(switch_port["number"])].name
        except:
            print("except?")
            print(switch_port["name"])
            continue
        switch_port["tags"] = configurations[switch_port["serial"] + str(switch_port["number"])].tags
        switch_port["enabled"] = configurations[switch_port["serial"] + str(switch_port["number"])].enabled
        switch_port["rstpEnabled"] = configurations[switch_port["serial"] + str(switch_port["number"])].rstp
        switch_port["stpGuard"] = configurations[switch_port["serial"] + str(switch_port["number"])].stp_guard
        switch_port["poeEnabled"] = configurations[switch_port["serial"] + str(switch_port["number"])].poe
        switch_port["type"] = configurations[switch_port["serial"] + str(switch_port["number"])].type
        switch_port["vlan"] = configurations[switch_port["serial"] + str(switch_port["number"])].vlan
        switch_port["voiceVlan"] = configurations[switch_port["serial"] + str(switch_port["number"])].voice_vlan
        switch_port["allowedVlans"] = configurations[
        switch_port["serial"] + str(switch_port["number"])].allowed_vlan

        # print switch_port["enabled"]

        print(switch_port["allowedVlans"])
        result = merakiapi.updateswitchport(api_key, switch_port["serial"], switch_port["number"], switch_port["name"],
                                   switch_port["tags"], switch_port["enabled"], switch_port["type"],
                                   switch_port["vlan"], switch_port["voiceVlan"], switch_port["allowedVlans"],
                                   switch_port["poeEnabled"], "", switch_port["rstpEnabled"],
                                   switch_port["stpGuard"],
                                   "")

        print(result)

    os.rename(temp_path, "app/archive/justafile.csv")
    return "IT WORKS!"


if __name__ == "__main__":
    main()

