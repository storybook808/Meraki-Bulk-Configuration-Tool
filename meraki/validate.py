#!/usr/bin/python3

#this reads a xlsx and validates it according to the parameters of each field

from openpyxl import workbook

#field properties
# Hostname: does not matter/any alphabet
# Serial #: 12 alpha numeric string with/without dashes in the middle
# Port #: just random number (i.e. 1-10)
# Name: does not matter
# Tags: does not matter
# Enabled: True/False in any form (caps, lowercase, upercase)
# RSTP: True/False in any form (caps, lowercase, upercase)
# STP Guard: disabled/root gound/ BPDU
# PoE: True/False in any form (caps, lowercase, upercase)
# Type: access/ trunk in any form (caps, lowercase, upercase)
# VLAN: just random number (i.e. 1-10)
# Voice VLAN: just random number (i.e. 1-10)
# Allowed VLANs: all/ comma seperated numbers (cannot read 000)

# reading in xlsx
wb = testing()

#grab the active worksheet
ws = wb.active

print(wb.active)