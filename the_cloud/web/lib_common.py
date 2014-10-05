# Copyright (C) 2012 Stephen Makonin. All Right Reserved.

import sys, os, hashlib, datetime, calendar
from datetime import timedelta
import MySQLdb as mdb

def gen_checksum(fn):
    fh = open(fn, 'rb')
    m = hashlib.md5()
    while True:
        data = fh.read(8192)
        if not data:
            break
        m.update(data)
    return m.hexdigest()

def get_one_value(con, sql, none_val):
    #print sql
    cur = con.cursor()
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    #print data
    if data == None:
        return none_val
    return data[0]

def auth_collector(con, collector, token):
    sql = "SELECT home_id FROM data_collector WHERE collector_id = '%s' AND token = '%s';" % (collector, token)
    return get_one_value(con, sql, "")

def auth_home(con, home, token):
    sql = "SELECT count(*) AS result FROM home WHERE home_id = '%s' AND token = '%s';" % (home, token)
    return get_one_value(con, sql, 0)

def get_last_counter(con, home, meter):
    sql = "SELECT COALESCE(MAX(counter), -1) AS counter FROM meter_counter WHERE home_id = '%s' AND meter_id = '%s';" % (home, meter)
    return float(get_one_value(con, sql, 0))

def get_accum(con, home, meter, counter):
    old_counter = get_last_counter(con, home, meter)

    if old_counter == -1:
        return 0;

    return counter - old_counter

def fix_value(v):
    if type(v).__name__ == "unicode":
        v = str(v)

    if type(v).__name__ == "str":
        if v[:1] == '!':
            return v[1:]
        else:
            return "'" + v + "'"

    return str(v)

def upd_table(con, table, keys, fields):
    into = ""
    set = ""
    select = ""
    where = ""

    for key in keys:
        into += key + ", "
        v = fix_value(keys[key])
        select += v + ", "
        where += key + " = " + v + " and "

    for field in fields:
        into += field + ", "
        v = fix_value(fields[field])
        select += v + ", "
        set += field + " = " + v + ", "

    into = into[:-2]
    set = set[:-2]
    select = select[:-2]
    where = where[:-5]

    sql = "INSERT INTO %s (%s) VALUES (%s) ON DUPLICATE KEY UPDATE %s;" % (table, into, select, set)
    #print sql
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    cur.close()

def upd_meter_counter(con, home, meter, ts, counter):
    accum = get_accum(con, home, meter, counter)
    
    keys = {'home_id': home, 'meter_id': meter}
    fields = {'counter': counter, 'read_dt': ts}
    upd_table(con, 'meter_counter', keys, fields)
    return accum


def upd_logs(con, home, meter, ts, accum, inst, amps):    
    year = "YEAR(CONVERT_TZ('%s', '+00:00', 'SYSTEM'))" % (ts)
    month =  "MONTH(CONVERT_TZ('%s', '+00:00', 'SYSTEM'))" % (ts)
    jday =  "DAYOFYEAR(CONVERT_TZ('%s', '+00:00', 'SYSTEM'))" % (ts)
    hour =  "HOUR(CONVERT_TZ('%s', '+00:00', 'SYSTEM'))" % (ts)
    minute =  "MINUTE(CONVERT_TZ('%s', '+00:00', 'SYSTEM'))" % (ts)
    new_ts = ts[0:-2] + "00" 
    
    cur = con.cursor()

    sql = "INSERT INTO log_yearly (home_id, meter_id, year, accum) VALUES ('%s', '%s', %s, %f) ON DUPLICATE KEY UPDATE accum = accum + %f;" % (home, meter, year, accum, accum)
    #print sql
    cur.execute(sql)
    sql = "INSERT INTO log_monthly (home_id, meter_id, year, month, accum) VALUES ('%s', '%s', %s, %s, %f) ON DUPLICATE KEY UPDATE accum = accum + %f;" % (home, meter, year, month, accum, accum)
    #print sql
    cur.execute(sql)
    sql = "INSERT INTO log_daily (home_id, meter_id, year, jday, accum) VALUES ('%s', '%s', %s, %s, %f) ON DUPLICATE KEY UPDATE accum = accum + %f;" % (home, meter, year, jday, accum, accum)
    #print sql
    cur.execute(sql)
    sql = "INSERT INTO log_hourly (home_id, meter_id, year, jday, hour, accum) VALUES ('%s', '%s', %s, %s, %s, %f) ON DUPLICATE KEY UPDATE accum = accum + %f;" % (home, meter, year, jday, hour, accum, accum)
    #print sql
    cur.execute(sql)
    sql = "INSERT INTO log_minutely (home_id, meter_id, year, jday, hour, minute, accum, inst) VALUES ('%s', '%s', %s, %s, %s, %s, %f, %f) ON DUPLICATE KEY UPDATE accum = accum + %f, inst = inst + %f;" % (home, meter, year, jday, hour, minute, accum, inst, accum, inst)
    #print sql
    cur.execute(sql)
    sql = "INSERT INTO log_last24hrs (home_id, meter_id, read_dt, accum, inst, amps) VALUES ('%s', '%s', '%s', %f, %f, %f) ON DUPLICATE KEY UPDATE accum = accum + %f, inst = inst + %f, amps = %f;" % (home, meter, new_ts, accum, inst, amps, accum, inst, amps)
    #print sql
    cur.execute(sql)
    sql = "DELETE FROM log_last24hrs WHERE home_id = '%s' AND meter_id = '%s' AND read_dt < NOW() - INTERVAL 1455 MINUTE;" % (home, meter)
    #print sql
    cur.execute(sql)

    con.commit()
    cur.close()

def upd_meter_pulse(con, home, meter, ts, pulses, avg, inst, min, max):
    accum = upd_meter_counter(con, home, meter, ts, pulses)

    keys = {'home_id': home, 'meter_id': meter, 'read_dt': ts}
    fields = {'pulses': pulses, 'avg_rate': avg, 'inst_rate': inst}
    upd_table(con, 'meter_pulse', keys, fields)

    upd_logs(con, home, meter, ts, accum, inst, 0.0)

    return accum

def upd_meter_power(con, home, meter, ts, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va):
    accum = upd_meter_counter(con, home, meter, ts, wh)
    inst = w
    
    keys = {'home_id': home, 'meter_id': meter, 'read_dt': ts}
    fields = {'v': v, 'a': a, 'freq': freq, 'pf_displ': pf_displ, 'pf_va': pf_va, 'wh': wh, 'w': w, 'varh': varh, 'var': var, 'vah': vah, 'va': va, }
    upd_table(con, 'meter_power', keys, fields)
    
    upd_logs(con, home, meter, ts, accum, inst, a)

    return accum
	
def upd_meter_soft(con, home, meter, ts, accum, inst, amps):
    upd_logs(con, home, meter, ts, accum, inst, amps)

def get_accum_max(con, home, meter, year, jday):
    sql = "SELECT MAX(accum) AS ACCUM FROM log_minutely WHERE home_id = '%s' AND meter_id = '%s' AND year = %d AND jday = %d;" % (home, meter, year, jday)
    return float(get_one_value(con, sql, 0))

def get_log_readings(con, home, dt, period, meters, cfactor):
    year = int(dt[:4])
    month = int(dt[5:7])
    day = int(dt[-2:])    
    dt_obj = datetime.datetime(year, month, day)    
    jday = dt_obj.timetuple()[7]
    mdays = calendar.monthrange(year, month)[1]
    first_jday = jday - day + 1 
    last_jday = jday + (mdays - day - 1)
    y_min = 9999999.9
    y_max = 0.0
    x_units = 0
    where = ""
    select = ""
    defaul_val = ""
    table = ""
    pdate = ""
    
    if period == "yearly":
        select = "month - 1"
        where = "year = %d" % (year)
        x_units = 12
        defaul_val = "0"
        table = "monthly"
        pdate = dt_obj.strftime("%Y")
    elif period == "monthly":
        select = "jday - %d" % (first_jday)
        where = "year = %d AND jday BETWEEN %d AND %d" % (year, first_jday, last_jday)
        x_units = 31
        defaul_val = "0"
        table = "daily"
        pdate = dt_obj.strftime("%B/%Y")
    elif period == "daily":
        select = "60 * hour + minute"
        where = "year = %d AND jday = %d" % (year, jday)
        x_units = 1440
        defaul_val = "null"
        table = "minutely"
        pdate = dt_obj.strftime("%A, %B %d, %Y")
    else:
        return None

    num_array = list()
    for i in range(x_units):
        num_array.append(defaul_val)
    
    sql = "SELECT %s AS xunit, SUM(accum) AS accum FROM log_%s WHERE home_id = '%s' AND meter_id IN (%s) AND %s GROUP BY xunit;" % (select, table, home, meters, where)
    #print sql
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    for row in rows:
        idx = int(row[0])
        num = float(row[1]) * cfactor #was abs() before
        num_array[idx] = str(num)

        if num < y_min:
            y_min = num
        if num > y_max:
            y_max = num

    cur.close()
    #print rows
    return (pdate, y_min, y_max, num_array)

def get_dates(con):
    sql = "SELECT CURDATE(), CURDATE() - INTERVAL 1 DAY;"
    #print sql
    cur = con.cursor()
    cur.execute(sql)
    data = cur.fetchone()
    cur.close()
    #print data
    return data

