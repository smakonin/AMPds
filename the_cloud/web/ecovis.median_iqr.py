# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

print "Content-type: application/json"
print

import sys, os, cgi, math, array, datetime, urllib, urllib2
from datetime import timedelta
from lib_config_msh import *
from lib_common import *


sql = "CALL ihd_agg();"
#print sql
cur = con.cursor()
cur.execute(sql)
rows = cur.fetchall()
json = ""
for row in rows:
    json = "{'Median': %d, 'Q1': %d, 'Q3': %d, 'IQR': %d, 'LowerBound': %d, 'UpperBound': %d, 'OnPeak': %d, 'Watts': %d} " % row

# clean up and exit
cur.close()
close_con()

print json

