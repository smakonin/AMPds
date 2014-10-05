# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

import sys, os, cgi, math, array, datetime, urllib, urllib2
from datetime import timedelta
from lib_config_msh import *
from lib_common import *


url = ""
power = []
sig = 0
sql = "SELECT inst AS power, accum AS energy, IF(CURTIME() BETWEEN '17:00' AND '19:00', 1, 0) AS pricing_sig FROM log_minutely WHERE inst >= 0 AND home_id = 'MAK' AND meter_id = 'MHE' ORDER BY year DESC, jday DESC, hour DESC, minute DESC LIMIT 0, 1;"
#print sql
cur = con.cursor()
cur.execute(sql)
rows = cur.fetchall()

for row in rows:
    power = {'value': [ int(row[0]), int(row[1]) ]};
    sig = {'value': int(row[2])};

# clean up and exit
close_con()

# send current power and energy readings
url = "https://api.electricimp.com/v1/523fdd160b0ce408/30107c1784f634d3"
req = urllib2.Request(url, urllib.urlencode(power))
response = urllib2.urlopen(req)
the_resp = response.read()

# send pricing signal
url = "https://api.electricimp.com/v1/523fdd160b0ce408/301a697b4116ee9c"
req = urllib2.Request(url, urllib.urlencode(sig))
response = urllib2.urlopen(req)
the_resp = response.read()

