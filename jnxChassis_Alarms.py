# Description:
        # This script is written for Juniper MX204 chassis alarm (Red and Yellow state).
        # Juniper Chassis Alarm Red State OID: .1.3.6.1.4.1.2636.3.4.2.3.1.0
        # Juniper Chassis Alarm Red State OID: .1.3.6.1.4.1.2636.3.4.2.2.1.0

# Usage: To use this script you need to put script in /var/run/scripts/snmp directory on MX204 device.

# Configuration: To get this script working you need to do same configuration on Juniper MX204:
        # set system scripts snmp file <script_name.py> oid <.OID>
        # set system scripts snmp file <script_name.py> python-script-user <user_name> (user must be super-user)
        # set system scripts language python3
        # (Optional) set system scripts snmp file <script_name.py> checksum sha-256 <checksum_value>

# Configuration Example:
    	# set system scripts language python3
    	# set system scripts snmp file jnxChassis_Alarms.py oid .1.3.6.1.4.1.2636.3.4.2.3.1.0
    	# set system scripts snmp file jnxChassis_Alarms.py oid .1.3.6.1.4.1.2636.3.4.2.2.1.0
    	# set system scripts snmp file jnxChassis_Alarms.py python-script-user admin
    	# (Optional) set system scripts snmp file jnxChassis_Alarms.py checksum sha-256 293479fcbede1c827062edbc764ad28cdec953202a72bdfe44f9c08a82b80270

# Alarm Values:
    	# 2 - Alarm OFF
    	# 3 - Alarm ON

# OID sources:
    	# jnxRedAlarmState: https://apps.juniper.net/mib-explorer/search.jsp#object=jnxRedAlarmState&product=Junos%20OS&release=20.3R3
   	# jnxYellowAlarmState: https://apps.juniper.net/mib-explorer/search.jsp#object=jnxYellowAlarmState&product=Junos%20OS&release=20.3R3

import jcs
from jnpr.junos import Device

def main():
    snmp_action = jcs.get_snmp_action()
    snmp_oid = jcs.get_snmp_oid()

# Find Chassis Red Alarm state
    with Device() as jdev:
        alarm_status_red = jdev.cli('show chassis alarms', warning=False)
    if alarm_status_red.find('Major') == -1:
        alarm_status_red = 2
    else:
        alarm_status_red = 3
    jcs.syslog("8", "snmp_action = ", snmp_action, " snmp_oid = ", snmp_oid)

# Find Chassis Yellow Alarm state
    with Device() as jdev:
        alarm_status_yellow = jdev.cli('show chassis alarms', warning=False)
    if alarm_status_yellow.find('Minor') == -1 and alarm_status_yellow.find('Medium') == -1:
        alarm_status_yellow = 2
    else:
        alarm_status_yellow = 3

#Red Alarm State OID Generator
    if snmp_action == 'get':
        if snmp_oid == '.1.3.6.1.4.1.2636.3.4.2.3.1.0':
            jcs.emit_snmp_attributes(snmp_oid, "Integer32", f"{alarm_status_red}")
    elif snmp_action == 'get-next':
        if snmp_oid == '.1.3.6.1.4.1.2636.3.4.2.3.1':
            jcs.emit_snmp_attributes(".1.3.6.1.4.1.2636.3.4.2.3.1.0", "Integer32", f"{alarm_status_red}")

# Yellow Alarm state OID Generator
    if snmp_action == 'get':
        if snmp_oid == '.1.3.6.1.4.1.2636.3.4.2.2.1.0':
            jcs.emit_snmp_attributes(snmp_oid, "Integer32", f"{alarm_status_yellow}")
    elif snmp_action == 'get-next':
        if snmp_oid == '.1.3.6.1.4.1.2636.3.4.2.2.1':
            jcs.emit_snmp_attributes(".1.3.6.1.4.1.2636.3.4.2.2.1.0", "Integer32", f"{alarm_status_yellow}")

if __name__ == '__main__':
    main()
