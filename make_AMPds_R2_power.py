#!/usr/bin/env python3
#
#    A utility of make the AMPds Release 2 public dataset: power meter data (make_AMPds_R2_power.py)
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

rawdata = './dump.R2/%s.csv' # localtion of db dump files
output = '/Users/stephen/Desktop/public/Electricity_%s.csv' # location to store new dataset files
# NOTE: the main house's energy is: MHE = WHE - (RSE + GRE), noise or unmtered UNE is WHE - sum(all sub-meters)
#       these are not included as files (1) to save space and (2) because they are easily calculable
#       MHE and UNE are sof-meters as the amounts are not from physical sensors, but software calculated
meter_ids = ['WHE', 'RSE', 'GRE', 'B1E', 'BME', 'CWE', 'DWE', 'EQE', 'FRE', 'HPE', 'OFE', 'UTE', 'WOE', 'B2E', 'CDE', 'DNE', 'EBE', 'FGE', 'HTE', 'OUE', 'TVE']
agg_meter = 'WHE'

# Raw data line are: timestamp, datetime, counter, averge rate, instantaneous rate
# Line data type:    int, str, float, float, float     
# Example:           1332411480,2012-03-22 03:18:00,40086.936,0,0
# NOTE: unix_ts from database dump file was calculated wrong by MySQL. Column 1 in in local time and column 2 is in UTC time.
column_ids = ['unix_ts', 'V', 'I', 'f', 'DPF', 'APF', 'P', 'Pt', 'Q', 'Qt', 'S', 'St']


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
print()
print('PASS 1: loading power meter data into correct time slots...')
meter_data = {}
meter_issues = {'missing 1 reading': 0, 'missing >1 reading': 0, 'multiple same unix_ts': 0, 'I resum amount': 0, 'P resum amount': 0, 'Q resum amount': 0, 'S resum amount': 0, 'got zero value': 0}
for (m, meter_id) in enumerate(meter_ids):
    meter_data[meter_id] = [[]] * minute_len
    
    filename = rawdata % meter_id
    print('\tLoading file:', filename)
    fp = open(filename, 'r')
    csvreader = csv.reader(fp)
    
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
         
        if meter_data[meter_id][i] == []:
            meter_data[meter_id][i] = [str(unix_ts), float(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]), int(line[8]), int(line[7]), int(line[10]), int(line[9]), int(line[12]), int(line[11])]
        else:
            print('\tIGNORE: unix timestamp', unix_ts, 'has multiple entries!', line)
            meter_issues['multiple same unix_ts'] += 1

    fp.close()

print()
print('PASS 2: wrangle missing/incorrect data...')
for tick in range(minute_len):
    unix_ts    = start_ts + tick * 60 # calc the curent timestamp based on the current tick
    incomplete = 0
    got0       = False
    _ts        = ''   # unix utc timestamp
    _v         = 0.0  # voltage
    _i         = 0.0  # current
    _f         = 0.00 # frequency
    _dpf       = 0.00 # dispacment power factor
    _apf       = 0.00 # apparent power factor
    _p         = 0    # real power
    _pt        = 0    # real energy
    _q         = 0    # reactive power
    _qt        = 0    # reactive energy
    _s         = 0    # apparent power
    _st        = 0    # apparent energy
    
    for i, meter_id in enumerate(meter_ids):
        if meter_data[meter_id][tick] == []:
            incomplete += 1
            meter_data[meter_id][tick] = list(meter_data[meter_id][tick-1])
            meter_data[meter_id][tick][0] = '+' + str(unix_ts)
            meter_data[meter_id][tick][7]  = '0' # Pt
            meter_data[meter_id][tick][9]  = '0' # Qt
            meter_data[meter_id][tick][11] = '0' # St
        else:
            if meter_data[meter_id][tick][1] == 0:
                got0  = True
            
            if tick > 0 and meter_data[meter_id][tick-1][0][:1] == '+':
                hist = 0
                for hist in range(tick - 1, 0, -1):
                    if meter_data[meter_id][hist][0][:1] != '+':
                        break;
                diff = tick - hist
                print('\tFIXING: missing readings for', meter_id, 'from', meter_data[meter_id][hist], 'to', meter_data[meter_id][tick], 'a gap of', diff)

                #if 1 < diff < 10:
                _pt = (meter_data[meter_id][tick][7] - meter_data[meter_id][hist][7]) / diff
                _qt = (meter_data[meter_id][tick][9] - meter_data[meter_id][hist][9]) / diff
                _st = (meter_data[meter_id][tick][11] - meter_data[meter_id][hist][11]) / diff
                
                for j in range(1, diff):
                    meter_data[meter_id][hist+j][7] = meter_data[meter_id][hist][7] + int(_pt * j)
                    meter_data[meter_id][hist+j][9] = meter_data[meter_id][hist][9] + int(_qt * j)
                    meter_data[meter_id][hist+j][11] = meter_data[meter_id][hist][11] + int(_st * j)
                #else:
                #    print('\tERROR: at unix_ts', meter_data[meter_id][tick][1], 'for meter', meter_id, 'diff of', diff, 'too big!')
                #    exit(1)

        if i == 0:            
            (_ts, _v, _i, _f, _dpf, _apf, _p, _pt, _q, _qt, _s, _st) = meter_data[meter_id][tick]

            if unix_ts != int(_ts):
                print('\tERROR: timestamp miss-match we calulated', unix_ts, 'but records have', _ts, '!')
                exit(1)
        else:
            _i = round(_i - meter_data[meter_id][tick][2], 1)
            _p -= meter_data[meter_id][tick][6]
            _q -= meter_data[meter_id][tick][8]
            _s -= meter_data[meter_id][tick][10]            
    
    if _i < 0:
        meter_issues['I resum amount'] += 1
        old_agg = meter_data[agg_meter][tick][2]
        new_agg = round(old_agg - _i, 1);
        meter_data[agg_meter][tick][2] = new_agg
        print('\tFIXING: unix_ts %d new I aggregate: %5.1fA -> %5.1fA!' % (unix_ts, old_agg, new_agg))
     
    if _p < 0:
        meter_issues['P resum amount'] += 1
        meter_data[agg_meter][tick][6] = meter_data[agg_meter][tick][6] - _p;

    if _q < 0:
        meter_issues['Q resum amount'] += 1
        meter_data[agg_meter][tick][8] = meter_data[agg_meter][tick][8] - _q;

    if _s < 0:
        meter_issues['S resum amount'] += 1
        meter_data[agg_meter][tick][10] = meter_data[agg_meter][tick][10] - _s;

    if incomplete == 1:
        meter_issues['missing 1 reading'] += 1
    elif incomplete > 1:
        meter_issues['missing >1 reading'] += 1
    
    if got0:
        print('\tFOUND: unix_ts %d voltage was zero!' % (unix_ts))
        meter_issues['got zero value'] += 1

# DONE clean up, now save dataset file (1 file per meter)
print()
print('Save wrangled dataset meter files...')
for (m, meter_id) in enumerate(meter_ids):
    filename = output % meter_id
    print('\tSaving file:', filename)
    fp = open(filename, 'w')    
    fp.write(','.join(column_ids) + '\n')
    for row in meter_data[meter_id]:
        fp.write(','.join([str(col) for col in row]) + '\n')
    fp.close()


# make measurement summary data
print()
print('Creating measurement summary data for easy of use...')
measure_ids = ['I', 'P', 'Q', 'S']
measure_cols = [2, 6, 8, 10]
measure_round = [True, False, False, False]
meter_cols = ['UNIX_TS', 'WHE', 'RSE', 'GRE', 'MHE', 'B1E', 'BME', 'CWE', 'DWE', 'EQE', 'FRE', 'HPE', 'OFE', 'UTE', 'WOE', 'B2E', 'CDE', 'DNE', 'EBE', 'FGE', 'HTE', 'OUE', 'TVE', 'UNE']
agg_idx = meter_cols.index('WHE')
une_idx = meter_cols.index('UNE')
mhe_idx = meter_cols.index('MHE')
for (m, measure_id) in enumerate(measure_ids):
    filename = output % measure_id
    print('\tCollecting and sroting', measure_id, 'data in file:', filename)
    fp = open(filename, 'w')    
    fp.write(','.join(meter_cols) + '\n')

    for i in range(minute_len):
        measure_data = [0] * len(meter_cols)
        measure_data[0] = meter_data[agg_meter][i][0]
        
        for meter_id in meter_ids:
            idx = meter_cols.index(meter_id)
            measure_data[idx] = meter_data[meter_id][i][measure_cols[m]]

        #import pdb; pdb.set_trace()
        
        measure_data[une_idx] = measure_data[agg_idx] - sum(measure_data[agg_idx+1:])
        measure_data[mhe_idx] = sum(measure_data[mhe_idx+1:])
        if measure_round[m]:
            measure_data[une_idx] = round(abs(measure_data[une_idx]), 1)
            measure_data[mhe_idx] = round(abs(measure_data[mhe_idx]), 1)
            
        fp.write(','.join([str(col) for col in measure_data]) + '\n')

    fp.close()


print()
print('ISSUE TALLIES OVER ALL METERS:')
print()
print(''.join(['%-32s = %8d\n' % (i, v) for (i, v) in meter_issues.items()]))

print()
print()
print('DONE!')
print()
print()
    
    
    
    
    