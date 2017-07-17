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

workbook = xlrd.open_workbook('testing.xlsx')
worksheet = wogit rkbook.sheet_by_index(0)

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
        print ('ERROR! Enabled must be either True or False')
        flag += 1
    if k == 1 or k == 0 or k == '':
        pass
    else:
        print('ERROR! RSTP must be either True or False')
        flag += 1
    if m == 1 or m == 0 or m == '':
        pass
    else:
        print('ERROR! PoE must be either True or False')
        flag += 1

    #for checking that serial # is a 12 alpha numberic string
    # grab value for serial number
    l = worksheet.cell(row, 1)
    if (len(l.value.lower().replace('-', '')) == 12):
        if l.ctype == 1 or l.ctype == 0:
            pass
        else:
            print("ERROR! Serial number must be a 12 character alpha numeric string")
            flag += 1
    else:
        print("ERROR! Serial number must be a 12 character alpha numeric string")
        flag += 1

    # for checking that STP Guard must be 'disabled' 'root gound' or 'BPDU'
    # grab value for STP Guard
    n = worksheet.cell(row, 7)
    if n.value.lower() == "disabled" or n.value.lower() == 'root guard' or n.value.lower() == 'bpdu guard' or n.value.lower() == '':
        pass
    else:
        print("""ERROR! STP Guard must be 'disabled' 'Root guard' or 'BPDU guard'""")
        flag += 1

    #for checking that Type is either access or trunk
    # grab value for type
    o = worksheet.cell(row, 9)
    if o.value == "trunk" or o.value == "access" or o.value == '':
        pass
    else:
        print("ERROR! Type must be either access or trunk")
        flag += 1

    # for checking that VLAN is a number
    # grab value for VLAN
    p = worksheet.cell(row, 10)
    # print(p.value)
    if p.ctype == 0 or p.ctype == 2:
        pass
    else:
        print("ERROR! VLAN must be a number")
        flag += 1

    #for checking that Voice VLAN must be a number
    # grab value for Voice VLAN
    q = worksheet.cell(row, 11)
    if q.ctype == 0 or q.ctype == 2:
        pass
    else:
        print("ERROR! Voice VLAN must be a number")
        flag += 1


    #for checking that Port # must be a number
    # grab value for port #
    r = worksheet.cell(row, 2)
    if r.ctype == 0 or r.ctype == 2:
        pass
    else:
        print("ERROR! Port # must be a number")
        flag += 1

    #for checking that Allowed VLANs can be all or comma seperated numbers
    # grab value for allowed VLANS
    s = worksheet.cell(row, 12)
    if s.ctype == 0 or s.ctype == 1 and s.value == 'all' or s.ctype == 2 or s.value == '':
        pass
    else:
        print("ERROR! Allowed VLANs must be 'all' or numbers")
        flag += 1

# if no error messages then display validation complete
if flag == 0:
    print('Validation Complete')