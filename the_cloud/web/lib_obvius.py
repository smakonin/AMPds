# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

import sys, os, csv
from lib_common import *

def read_csv_file(con, home, device_class, modbus_id, filename):
    for row in csv.reader(open(filename, 'rU')):
        if device_class == 52:
            proc_dent_powerscout_18(con, home, modbus_id, row)
        elif device_class == 67:
            proc_obvius_a7810_pulses(con, home, modbus_id, row)
        else:
            return 0

    return 1

def proc_dent_powerscout_18(con, home, modbus_id, row):
    meter = ""
    if modbus_id == 1:
        meter = ("M_E","","","")
    elif modbus_id == 2:
        meter = ("RSE","","","")
    elif modbus_id == 3:
        meter = ("GRE","","","")
    elif modbus_id == 4:
        meter = ("HPE","","","")
    elif modbus_id == 5:
        meter = ("CDE","","","")
    elif modbus_id == 6:
        meter = ("WOE","","","")
    elif modbus_id == 7:
        meter = ("","B1E","B2E","TVE")
    elif modbus_id == 8:
        meter = ("","DWE","CTE","OUE")
    elif modbus_id == 9:
        meter = ("","BME","EBE","FRE")
    elif modbus_id == 10:
        meter = ("","DNE","UTE","LIE")
    elif modbus_id == 11:
        meter = ("","FGE","MWE","HTE")
    elif modbus_id == 12:
        meter = ("","OFE","CWE","EQE")
    
    ts = row[0].replace("'", "")
    status = int(row[1])
    if status != 0:
        return
    
    if meter[0] != "":
        v = round(float(row[50] or 0), 3) + round(float(row[51] or 0), 3)
        a = round(float(row[16] or 0), 3)
        freq = round(float(row[22] or 0), 3)
        pf_displ = round(float(row[14] or 0), 3)
        pf_va = round(float(row[15] or 0), 3)
        wh = round(float(row[4] or 0) * 1000, 3)
        w = round(float(row[5] or 0) * 1000, 3)
        varh = round(float(row[10] or 0) * 1000, 3)
        var = round(float(row[11] or 0) * 1000, 3)
        vah = round(float(row[12] or 0) * 1000, 3)
        va = round(float(row[13] or 0) * 1000, 3)
        
        accum = upd_meter_power(con, home, meter[0], ts, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va)
        inst = w
        
        if meter[0] == "M_E":
            upd_meter_soft(con, home, "MHE", ts, accum, inst, a)
            upd_meter_soft(con, home, "OTE", ts, accum, inst, a)
        elif meter[0] == "RSE" or meter[0] == "GRE":
            upd_meter_soft(con, home, "MHE", ts, -accum, -inst, -a)
            upd_meter_soft(con, home, "OTE", ts, -accum, -inst, -a)
        else:
            upd_meter_soft(con, home, "OTE", ts, -accum, -inst, -a)
    else:
        for sub in range(3):
            v = round(float(row[50 + sub] or 0), 3)
            a = round(float(row[47 + sub] or 0), 3)
            freq = round(float(row[22] or 0), 3)
            pf_displ = round(float(row[41 + sub] or 0), 3)
            pf_va = round(float(row[44 + sub] or 0), 3)
            wh = round(float(row[23 + sub] or 0) * 1000, 3)
            w = round(float(row[26 + sub] or 0) * 1000, 3)
            varh = round(float(row[29 + sub] or 0) * 1000, 3)
            var = round(float(row[32 + sub] or 0) * 1000, 3)
            vah = round(float(row[35 + sub] or 0) * 1000, 3)
            va = round(float(row[38 + sub] or 0) * 1000, 3)
            
            accum = upd_meter_power(con, home, meter[sub + 1], ts, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va)
            inst = w
            
            upd_meter_soft(con, home, "OTE", ts, -accum, -inst, -a)

def proc_obvius_a7810_pulses(con, home, modbus_id, row):
    ts = row[0].replace("'", "")
    status = int(row[1])
    if status != 0:
        return
    
    p1_tc = round(float(row[4] or 0), 3)
    p1_ar = round(float(row[5] or 0), 3)
    p1_ir = round(float(row[6] or 0), 3)
    p1_lr = round(float(row[7] or 0), 3)
    p1_hr = round(float(row[8] or 0), 3)
    
    p2_tc = round(float(row[9] or 0), 3)
    p2_ar = round(float(row[10] or 0), 3)
    p2_ir = round(float(row[11] or 0), 3)
    p2_lr = round(float(row[12] or 0), 3)
    p2_hr = round(float(row[13] or 0), 3)
    
    p3_tc = round(float(row[14] or 0), 3)
    p3_ar = round(float(row[15] or 0), 3)
    p3_ir = round(float(row[16] or 0), 3)
    p3_lr = round(float(row[17] or 0), 3)
    p3_hr = round(float(row[18] or 0), 3)
    
    p4_tc = round(float(row[19] or 0), 3)
    p4_ar = round(float(row[20] or 0), 3)
    p4_ir = round(float(row[21] or 0), 3)
    p4_lr = round(float(row[22] or 0), 3)
    p4_hr = round(float(row[23] or 0), 3)
    
    upd_meter_pulse(con, home, "M_W", ts, p1_tc, p1_ar, p1_ir, p1_lr, p1_hr)
    upd_meter_pulse(con, home, "HTW", ts, p2_tc, p2_ar, p2_ir, p2_lr, p2_hr)
    upd_meter_pulse(con, home, "M_G", ts, p3_tc, p3_ar, p3_ir, p3_lr, p3_hr)
    upd_meter_pulse(con, home, "FRG", ts, p4_tc, p4_ar, p4_ir, p4_lr, p4_hr)
