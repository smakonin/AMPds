#!/usr/bin/env python3
#
#    A utility of make the AMPds Release 2 public dataset: water and natural gas pulse meter data (make_AMPds2_pulse.py)
#
#    Copyright (C) 2015 Stephen Makonin. All Right Reserved.
#

import os, math, csv, time
from datetime import datetime
from calendar import timegm


# set the proper timezone to location of testing house
os.environ['TZ'] = 'America/Vancouver'
time.tzset()
print('Timezone set to:', time.tzname)

step = 60 # seconds in a minute
min_per_year = 525600 # 1 year in minutes
years = 2 # number of years to store
minute_len = int(min_per_year * years) # calc number of minues to store
start_ts = 1333263600 # the start timespamp: April 1, 2012 00:00:00 pacific time
end_ts = start_ts + (minute_len - 1) * step # calc end timestampe

issues = {'multiple same unix_ts': 0, 'missing unix_ts': 0, 'counter reset': 0, 'avg_rate rounding/mismatch': 0}

rawdata = './dump.R2/%s.csv' # localtion of db dump files
output = '/Users/stephen/Desktop/public/%s_%s.csv' # location to store new dataset files
meter_ids = ['WHW', 'HTW', 'WHG', 'FRG']
consumable = ['Water', 'Water', 'NaturalGas', 'NaturalGas']
time_measure = [1, 1, 60, 60] # where: 1 = /minute, 60 = /hour

# Raw data line are: timestamp, datetime, counter, averge rate, instantaneous rate
# Line data type:    int, str, float, float, float     
# Example:           1332411480,2012-03-22 03:18:00,40086.936,0,0
# NOTE: unix_ts from database dump file was calculated wrong by MySQL. Column 1 in in local time and column 2 is in UTC time.
column_ids = ['unix_ts', 'counter', 'avg_rate', 'inst_rate']

''' I REALLY DO NOT LIKE TIMEZONES WITH TIME CHANGES!

>>> d = '2012-04-01 00:00:00 UTC'
>>> dt = datetime.strptime(d, '%Y-%m-%d %H:%M:%S %Z')
>>> timegm(dt.utctimetuple())
1333238400
>>> tt = timegm(dt.utctimetuple())
>>> time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tt))
'2012-03-31 17:00:00'
>>> time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(tt))
'2012-04-01 00:00:00'
>>>

Human date to Timestamp
Epoch timestamp: 1333263600
Timestamp in milliseconds: 1333263600000
Human time (your time zone): April 1, 2012 at 12:00:00 AM PDT
Human time (GMT): Sun, 01 Apr 2012 07:00:00 GMT

Epoch timestamp: 1333238400
Timestamp in milliseconds: 1333238400000
Human time (GMT): Sun, 01 Apr 2012 00:00:00 GMT
Human time (your time zone): March 31, 2012 at 5:00:00 PM PDT
'''

# load all raw meter data and do
for (m, meter_id) in enumerate(meter_ids):
    meter_data = [[]] * minute_len
    meter_issues = dict(issues)

    print()
    print('Start wrangling', consumable[m], 'meter', meter_id, 'with', ('/minute' if time_measure[m] == 1 else '/hour'), 'rates and', minute_len, 'reading(s)...')

    # PASS 1: convert data to proper dataypes, missing time stamps will be []
    print('\tBegining PASS 1 cleanup...')
    
    filename = rawdata % meter_id
    print('\tLoading file:', filename)
    fp = open(filename, 'r')
    csvreader = csv.reader(fp)
    
    first_line = True
    for line in csvreader:
        
        # convert the db dump text date time to a unix UTC int timestamp
        utc_tm = str(line[1])
        # zero out teh seconds and add UTC timezone
        utc_tm = utc_tm[:-2] + '00 UTC'
        dt = datetime.strptime(utc_tm, '%Y-%m-%d %H:%M:%S %Z')
        unix_ts = timegm(dt.utctimetuple())

        if unix_ts < start_ts:
            continue
        if unix_ts > end_ts:
            break;

        i = (unix_ts - start_ts) // step
        local_tm = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unix_ts))
        counter = float(line[2])
        avg_rate = float(line[3])
        inst_rate = float(line[4])
        
        if meter_data[i] == []:
            meter_data[i] = [unix_ts, counter, avg_rate, inst_rate]
        else:
            print('\tIGNORE: unix timestamp', unix_ts, 'has multiple entries!', line)
            meter_issues['multiple same unix_ts'] += 1

    fp.close()


    # PASS 2: check from coutner resets and fix
    print()
    print('\tBegining PASS 2 cleanup...')
    end = start = -1
    reset_incro = 0
    for i in range(1, len(meter_data)):
        if meter_data[i] == []:
            meter_issues['missing unix_ts'] += 1
            if start == -1:
                start = i - 1
            end = i
        else:
            # to remove resets, make sure teh counter is always increasing 
            meter_data[i][1] = round(meter_data[i][1] + reset_incro, 3)
                        
            if start != -1:
                missing_gap = end - start
                print('\tFIXING: missing readings from', meter_data[start], 'to', meter_data[i], 'a gap of', missing_gap)
                counter = meter_data[start][1]
                avg_rate = 0.0 
                inst_rate = 0.0
                for j in range(start + 1, end):
                    unix_ts = start_ts + j * step
                    meter_data[j] = ['+' + str(unix_ts), counter, avg_rate, inst_rate]
                
                delta = round(meter_data[i][1] - meter_data[start][1], 3)
                if delta < 0:
                    print('\tFIXING: counter reset!', meter_data[start], meter_data[i])
                    meter_issues['counter reset'] += 1
                    counter = meter_data[start][1]
                    amount = round(int(counter * 2) / 2 + 0.5, 1)
                    delta = round(amount - counter, 3)
                    reset_incro += round(amount - meter_data[i][1], 3)
                    meter_data[i][1] = round(meter_data[i][1] + reset_incro, 3)
                
                unix_ts = start_ts + end * 60
                counter = meter_data[i][1]
                delta = round(delta * time_measure[m], 3)
                meter_data[end] = ['+' + str(unix_ts), counter, delta, inst_rate]
                end = start = -1

            calc_avg_rate = round((meter_data[i][1] - meter_data[i-1][1]) * time_measure[m], 3)
            if calc_avg_rate != meter_data[i][2]:
                print('\tFIXING: avg_rate rounding/missmatch error of', round(abs(meter_data[i][2] - calc_avg_rate), 3), '!', meter_data[i])
                meter_issues['avg_rate rounding/mismatch'] += 1
                meter_data[i][2] = calc_avg_rate
                
                
    # DONE clean up, now save dataset file (1 file per meter)
    filename = output % (consumable[m], meter_id)
    print()
    print('\tSave wrangled dataset file:', filename)
    fp = open(filename, 'w')    
    fp.write(','.join(column_ids) + '\n')
    for row in meter_data:
        fp.write(','.join([str(col) for col in row]) + '\n')
    fp.close()


    print()
    print('\tISSUE TALLIES:')
    print()
    print('\t' + '\t'.join(['%-32s = %5d\n' % (i, v) for (i, v) in meter_issues.items()]))

print()
print()
print('DONE!')
print()
print()
