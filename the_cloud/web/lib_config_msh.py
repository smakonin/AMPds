# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

import MySQLdb as mdb

logfile = "./logs/device-log-reading.err"
lastfile = "./logs/device-log-reading.last"
con = mdb.connect('localhost', 'msh_ws_user', add-password-here, 'smarthome')

def close_con():
    global con
    con.close()
