# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

import sys, os, cgi, math, array, datetime, urllib, urllib2
from datetime import timedelta
from lib_config_msh import *
from lib_common import *


#sql = "CALL ihd_agg();"
sql = "select * from calc_ihd_agg;"
#print sql
cur = con.cursor()
cur.execute(sql)
rows = cur.fetchall()
json = ""
for row in rows:
    #json = "[%d, %d]" % (row[0], row[5])
    json = "[%d, %d]" % (row[2], row[7])

# clean up and exit
cur.close()
close_con()

print "Content-type: application/json"
print "content-length: %d" % (len(json))
print
print json

