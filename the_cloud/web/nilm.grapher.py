# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

print "Content-type: text/plain"
print

import sys, os, cgi, math, array, datetime
from datetime import timedelta
from lib_config_msh import *
from lib_common import *

query = os.environ['QUERY_STRING']
qs = cgi.parse_qs(query)
id = qs['id'][0]
start = qs['start'][0]
end = qs['end'][0]
type = qs['type'][0]
#id = "T"
#start = "2012-11-16 00:00:00"
#end = "2012-11-17 23:00:00"
#type = "amps"

home = "MAK"
data = ""
idTranslations = {'T': "'MHE'",
                  'H': "'HPE', 'FRE'", 
                  'K': "'FGE', 'CTE', 'DWE', 'WOE', 'MWE'",
                  'C': "'CDE', 'CWE'",
                  'O': "'OFE', 'B2E', 'DNE', 'EBE', 'EQE'",
                  'E': "'TVE'",
                  'R': "'OUE', 'B1E', 'BME', 'HTE', 'LIE', 'UTE'",
                  'U': "'OTE'"}

if type == 'accum' or type == 'inst' or type == 'amps':

    if type == 'amps':
        type = 'ROUND(' + type + ')'

    start_dt = datetime.datetime(int(start[:4]), int(start[5:7]), int(start[8:10]), int(start[11:13]), int(start[14:16]), int(start[-2:]))
    end_dt = datetime.datetime(int(end[:4]), int(end[5:7]), int(end[8:10]), int(end[11:13]), int(end[14:16]), int(end[-2:]))
    steps = end_dt - start_dt
    steps = int(steps.seconds / 60 + steps.days * 24 * 60)

    num_array = list()
    for i in range(steps):
        num_array.append("0")

    sql = "SELECT (UNIX_TIMESTAMP(read_dt) - UNIX_TIMESTAMP('%s')) / 60 as idx, sum(%s) FROM log_last24hrs WHERE home_id = '%s' AND meter_id IN (%s) AND read_dt BETWEEN '%s' AND ('%s' - INTERVAL 1 MINUTE) GROUP BY read_dt ORDER BY read_dt;" % (start, type, home, idTranslations[id], start, end)
    #print sql
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        idx = int(row[0])
        if idx >= 7640:
            idx -= 7640

        val = row[1]
        if val < 0:
            val = 0

        #print "row[0]=%d, idx=%d, row[1]=%s" % (int(row[0]), idx, str(row[1])) 
        num_array[idx] = str(int(val))

    data = ','.join(num_array)

# clean up and exit
close_con()
print data
