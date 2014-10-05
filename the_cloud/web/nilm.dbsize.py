# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

print "Content-type: text/plain"
print

import sys, os, cgi, math, array, datetime
from datetime import timedelta
from lib_config_msh import *
from lib_common import *

units = ('kB', 'MB', 'GB', 'TB')

sql = "SELECT table_schema, sum(data_length+index_length) as size, sum(data_free) as free FROM information_schema.TABLES WHERE table_schema = 'smarthome' GROUP BY table_schema;"
#print sql
cur = con.cursor()
cur.execute(sql)
rows = cur.fetchall()

for row in rows:
    db_size = row[1]
    unit = "B"

    for i in range(len(units)):
        if db_size >= 1024:
            db_size /= 1024
            unit = units[i]

    #print "Database %s is %5.2f%s in size." % (row[0], db_size, unit)
    print "%.2f%s" % (db_size, unit)

# clean up and exit
close_con()
