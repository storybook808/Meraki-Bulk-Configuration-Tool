#!/usr/bin/python3

#this reads a xlsx and validates it according to the parameters of each field


#field properties
# Hostname: does not matter/any alphabet col 0
# Serial #: 12 alpha numeric string with/without dashes in the middle col 1
# Port #: just random number (i.e. 1-10) col 2
# Name: does not matter col 3
# Tags: does not matter col 4
# Enabled: True/False in any form (caps, lowercase, upercase) col 5
# RSTP: True/False in any form (caps, lowercase, upercase) col 6
# STP Guard: disabled/root gound/ BPDU col 7
# PoE: True/False in any form (caps, lowercase, upercase) col 8
# Type: access/ trunk in any form (caps, lowercase, upercase) col 9
# VLAN: just random number (i.e. 1-10) col 10
# Voice VLAN: just random number (i.e. 1-10) col 11
# Allowed VLANs: all/ comma seperated numbers (cannot read 000) col 12

import xlrd

workbook = xlrd.open_workbook('8P Port Configuration.xlsx')
worksheet = workbook.sheet_by_index(0)

flag = 0

# for T/F values: Enabled, RSTP and PoE
for row in range(1, worksheet.nrows):
    # grab value for enable
    enable = worksheet.cell_value(row, 5)
    # grab value for RSTP
    rstp = worksheet.cell_value(row, 6)
    # grab value for PoE
    poe = worksheet.cell_value(row, 8)
    if enable == 1 or enable == 0 or enable == '':
        pass
    else:
        print ('ERROR! Enabled must be either True or False')
        flag += 1
    if rstp == 1 or rstp == 0 or rstp == '':
        pass
    else:
        print('ERROR! RSTP must be either True or False')
        flag += 1
    if poe == 1 or poe == 0 or poe == '':
        pass
    else:
        print('ERROR! PoE must be either True or False')
        flag += 1

    #for checking that serial # is a 12 alpha numberic string
    # grab value for serial number
    serial_number = worksheet.cell(row, 1)
    if (len(serial_number.value.lower().replace('-', '')) == 12):
        if serial_number.ctype == 1 or serial_number.ctype == 0:
            pass
        else:
            print("ERROR! Serial number must be a 12 character alpha numeric string")
            flag += 1
    else:
        print("ERROR! Serial number must be a 12 character alpha numeric string")
        flag += 1

    # for checking that STP Guard must be 'disabled' 'root gound' or 'BPDU'
    # grab value for STP Guard
    stp_guard = worksheet.cell(row, 7)
    if stp_guard.value.lower() == "disabled" or stp_guard.value.lower() == 'root guard' or stp_guard.value.lower() == 'bpdu guard' or stp_guard.value.lower() == '':
        pass
    else:
        print("""ERROR! STP Guard must be 'disabled' 'Root guard' or 'BPDU guard'""")
        flag += 1

    #for checking that Type is either access or trunk
    # grab value for type
    type = worksheet.cell(row, 9)
    if type.value == "trunk" or type.value == "access" or type.value == '':
        pass
    else:
        print("ERROR! Type must be either access or trunk")
        flag += 1

    # for checking that VLAN is a number
    # grab value for VLAN
    vlan = worksheet.cell(row, 10)
    # print(p.value)
    if vlan.ctype == 0 or vlan.ctype == 2:
        pass
    else:
        print("ERROR! VLAN must be a number")
        flag += 1

    #for checking that Voice VLAN must be a number
    # grab value for Voice VLAN
    voice_vlan = worksheet.cell(row, 11)
    if voice_vlan.ctype == 0 or voice_vlan.ctype == 2:
        pass
    else:
        print("ERROR! Voice VLAN must be a number")
        flag += 1


    #for checking that Port # must be a number
    # grab value for port #
    port_number = worksheet.cell(row, 2)
    if port_number.ctype == 0 or port_number.ctype == 2:
        pass
    else:
        print("ERROR! Port # must be a number")
        flag += 1

    #for checking that Allowed VLANs can be all or comma seperated numbers
    # grab value for allowed VLANS
    allowed_vlans = worksheet.cell(row, 12) 
    if allowed_vlans.ctype == 0 or allowed_vlans.ctype == 1 or allowed_vlans.value == 'all' or allowed_vlans.ctype == 2 or allowed_vlans.value == '':
        pass
    else:
        print("ERROR! Allowed VLANs must be 'all' or numbers")
        flag += 1

# if no error messages then display validation complete
if flag == 0:
    print('Validation Complete')