# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

import sys, os, cgi, gzip, traceback
from lib_config_msh import *
from lib_obvius import *

filepath = ""

# exit with unauthorized error
def unauth():
    print "Status: 401 Access Denied"
    print
    sys.exit(0)

# exit with fail
def fail(reason):
    print "Status: 406 Not Acceptable"
    print "Content-type: text/plain"
    print
    print "FAILURE: %s" % (reason)
    print "NOTES:   Rejected logfile upload"
    sys.exit(0)

# exit with success
def success():
    print "Status: 200 OK"
    print "Content-type: text/plain"
    print
    print "SUCCESS"
    sys.exit(0)

# custom exception handler
_old_excepthook = sys.excepthook

def return_except(exctype, excval, exctb):
    global filepath

    if filepath != "":
        os.remove(filepath)

    fail("%s (line %d)" % (traceback.format_exception_only(exctype, excval), exctb.tb_lineno))

sys.excepthook = return_except

# load cgi form
form = cgi.FieldStorage()

# authenticate the data collector
home = auth_collector(con, form.getvalue('SERIALNUMBER'), form.getvalue('PASSWORD'))
if home == "":
    unauth()

# do a mode value check
if form.getvalue('MODE') == 'LOGFILEUPLOAD':
    # do nothing, we want this to happen
    happy = "joy"
elif form.getvalue('MODE') == 'STATUS':
    success()
elif form.getvalue('MODE') == 'TEST':
    success()
elif form.getvalue('MODE') == 'CONFIGFILEMANIFEST':
    success()
elif form.getvalue('MODE') == 'CONFIGFILEDOWNLOAD':
    success()
elif form.getvalue('MODE') == 'CONFIGFILEUPLOAD':
    success()
else:
    fail("Mode Type %s not supported." % (form.getvalue('MODE')))


# save file, rund checksum, uncompress
fileitem = form['LOGFILE']
filename = os.path.basename(fileitem.filename)
filepath = "/tmp/obvius/%s" % (filename)
open(filepath, 'wb').write(fileitem.file.read())
checksum = gen_checksum(filepath)
if form.getvalue('MD5CHECKSUM') != checksum:
    fail("Checksum mismatch remote[%s] = local[%s]" % (form.getvalue('MD5CHECKSUM'), checksum))
f = gzip.open(filepath, 'rb')
blob = f.read()
f.close()
open(filepath, 'w').write(blob)

# process the file and save in database
if read_csv_file(con, home, int(form.getvalue('MODBUSDEVICECLASS')), int(form.getvalue('MODBUSDEVICE')), filepath) == 0:
    fail("Device Class %d not supported." % (int(form.getvalue('MODBUSDEVICECLASS'))))

# clean up and exit
os.remove(filepath)
#os.rename(filepath, "/tmp/obvius/done/%s" % (filename))
close_con()
success()
