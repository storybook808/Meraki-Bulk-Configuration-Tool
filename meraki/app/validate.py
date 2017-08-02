from app import app
from flask import redirect, url_for, flash, Blueprint
import os


validate_blueprint = Blueprint('validate', __name__, template_folder='templates')

# Route to validation script


@validate_blueprint.route('/validate/')
def validate_form():
    import xlrd

    # open up working excel file to validate.
    # dictate path for excel file
    path = os.path.abspath(os.path.join('app', 'temp'))
    current_file = os.listdir(path)
    print(path + current_file[0])
    # open up working excel file to validate.
    workbook = xlrd.open_workbook(path + '/' + current_file[0])
    worksheet = workbook.sheet_by_index(1)

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
            flash('ERROR! Enabled must be either True or False. Check cell: F', row)
            flag += 1
        if rstp == 1 or rstp == 0 or rstp == '':
            pass
        else:
            flash('ERROR! RSTP must be either True or False. Check cell: G', row)
            flag += 1
        if poe == 1 or poe == 0 or poe == '':
            pass
        else:
            flash('ERROR! PoE must be either True or False. Check cell: I', row)
            flag += 1

        # for checking that STP Guard must be 'disabled' 'root gound' or 'BPDU'
        # grab value for STP Guard
        stp_guard = worksheet.cell(row, 7)
        if stp_guard.value.lower() == "disabled" or stp_guard.value.lower() == 'root guard' or stp_guard.value.lower() == 'bpdu guard' or stp_guard.value.lower() == '':
            pass
        else:
            flash("""ERROR! STP Guard must be 'disabled' 'Root guard' or 'BPDU guard'. Check cell: H""", row)
            flag += 1

        # for checking that Type is either access or trunk
        # grab value for type
        type = worksheet.cell(row, 9)
        if type.value.lower() == "trunk" or type.value.lower() == "access" or type.value.lower() == '':
            pass
        else:
            flash("ERROR! Type must be either access or trunk. Check cell: J", row)
            flag += 1

        # for checking that VLAN is a number
        # grab value for VLAN
        vlan = worksheet.cell(row, 10)
        if vlan.ctype == 0 or vlan.ctype == 2:
            pass
        else:
            flash("ERROR! VLAN must be a number. Check cell: K", row)
            flag += 1

        # for checking that Voice VLAN must be a number
        # grab value for Voice VLAN
        voice_vlan = worksheet.cell(row, 11)
        if voice_vlan.ctype == 0 or voice_vlan.ctype == 2:
            pass
        else:
            flash("ERROR! Voice VLAN must be a number. Check cell: L", row)
            flag += 1

        # for checking that Port # must be a number
        # grab value for port #
        port_number = worksheet.cell(row, 2)
        if port_number.ctype == 0 or port_number.ctype == 2:
            pass
        else:

            flash("ERROR! Port # must be a number. Check cell: C", row)
            flag += 1

        # for checking that Allowed VLANs can be all or comma seperated numbers
        # grab value for allowed VLANS
        allowed_vlan = worksheet.cell(row, 12)

        if allowed_vlan.ctype == 0 or allowed_vlan.ctype == 1 or allowed_vlan.value == 'all' or allowed_vlan.ctype == 2 or allowed_vlan.value == '':
            pass
        else:
            flash("ERROR! Allowed VLANs must be 'all' or numbers. Check cell: M", row)
            flag += 1

    # if no error messages then display validation complete
    if flag == 0:
        flash('Validation Complete')

    # return same template page to display messages
    return redirect(url_for('step2a'))

