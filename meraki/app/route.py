from app import app
from flask import render_template, request, redirect, url_for
from werkzeug import secure_filename
import os, shutil
import openpyxl


@app.route('/uploader', methods=['GET', 'POST'])
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

    file_rename()
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
