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
worksheet = workbook.sheet_by_index(0)

#for T/F values: Enabled, RSTP and PoE
for row in range(1, worksheet.nrows):
    # grab value for enable
    j = worksheet.cell_value(row, 5)
    # grab value for RSTP
    k = worksheet.cell_value(row, 6)
    # grab value for PoE
    m = worksheet.cell_value(row, 8)
    print (j, k, m)

    if j == 1 or j == 0 or j == '':
        pass
    else:
        print('Enabled must be either True or False')
        break
    if k == 1 or k == 0 or k == '':
        pass
    else:
        print('RSTP must be either True or False')
        break
    if m == 1 or m == 0 or m == '':
        pass
    else:
        print('PoE must be either True or False')
        break
print('Enabled, RSTP and PoE is done')


# for checking that serial # is a 12 alpha numberic string
for row in range(1, worksheet.nrows):
    l = worksheet.cell(row, 1)
    print(l.value)



# for checking that STP Guard must be 'disabled' 'root gound' or 'BPDU'
for row in range(1, worksheet.nrows):
    n = worksheet.cell(row, 7)
    print(n.value.lower())
    if n.value == "disabled" or n.value == 'root guard' or n.value == 'bpdu guard' or n.value == '':
        print('this is right!')
        pass
    else:
        print("""STP Guard must be 'disabled' 'Root guard' or 'BPDU guard'""")
        break
print('STP Guard is done')

# for checking that Type is either access or trunk
for row in range(1, worksheet.nrows):
    o = worksheet.cell(row, 9)
    print(o.value)
    if o.value == "trunk" or o.value == "access" or o.value == '':
        pass
    else:
        print("Type much be either access or trunk")
        break
print('Type is done')