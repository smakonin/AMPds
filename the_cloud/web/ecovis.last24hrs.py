# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

print "Content-type: text/plain"
print

import sys, os, cgi, math, array, datetime
from datetime import timedelta
from lib_config_msh import *
from lib_common import *

#dt = ""
#try:
#    query = os.environ['QUERY_STRING']
#    qs = cgi.parse_qs(query)
#    dt = qs['date'][0]
#except:
#    dt = ""

home = "MAK"
ce_meters = (('MHE', ''), ('HPE', 'FRE'), ('FGE', 'CTE', 'DWE', 'WOE', 'MWE'), ('CDE', 'CWE'), ('OFE', 'B2E', 'DNE', 'EBE', 'EQE'), ('TVE', ''), ('OUE', 'B1E', 'BME', 'HTE', 'LIE', 'UTE', 'OTE'))
ce_names = ('All', 'HVAC', 'Kitchen', 'Cloths', 'Computer', 'Ent/TV', 'Other')


def get_log_last24hrs(con, home, meters, cfactor):
    max_idx = 24

    num_array = list()
    for i in range(max_idx):
        num_array.append(0)

    sql = "SELECT year, jday, hour, SUM(accum) AS accum FROM log_hourly WHERE home_id = '%s' AND meter_id IN (%s) GROUP BY year DESC, jday DESC, hour DESC LIMIT %d;" % (home, meters, max_idx)
    #print sql
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    idx = max_idx;
    for row in rows:
        num = float(row[3]) * cfactor
        num_array[idx - 1] = str(num)
        idx -= 1

    return num_array

count = 0;
for meter in ce_meters:
    txt_meter = "'%s'" % ("','".join(meter))
    num_array = get_log_last24hrs(con, home, txt_meter, 1.000)
    print "%s,%s,%s" % (meter[0].lower(), ce_names[count], ",".join(num_array))
    count += 1;

# clean up and exit
close_con()
