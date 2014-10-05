#!/usr/bin/env python3
#
#    A utility of make the AMPds public dataset (Make_AMPds_Release.py)
#
#    Version 2: Copyright (C) 2014 Stephen Makonin. All Right Reserved.
#    Version 1: Copyright (C) 2013 Stephen Makonin. All Right Reserved.
#    

import math, csv, pytz
from datetime import *

def load_csv(filename, limit=0):
    print('Loading file:', filename)
    fp = open(filename, 'r')
    csvreader = csv.reader(fp)

    count = 0
    data = []
    for row in csvreader:
        data.append([col for col in row])
        count += 1
        if limit > 0 and count >= limit:
            break
        
    fp.close()
    return data

#ts,pulses,avg_rate,inst_rate     ---accum
def save_power_csv(filename, data):
    print('Saving file:', filename)
    fp = open(filename, 'w')
    fp.write('  TIMESTAMP,     V,     I,     f,  DPF,  APF,     P,            Pt,     Q,            Qt,     S,            St\n')
    for d in data:
        fp.write('%1s%10d, %5.1f, %5.1f, %5.2f, %0.2f, %0.2f, %5d, %13d, %5d, %13d, %5d, %13d\n' % (d[-1], int(d[0]), round(float(d[1]), 1), round(float(d[2]), 1),  round(float(d[3]), 2), round(float(d[4]), 2), round(float(d[5]), 2), int(d[7]), int(d[6]), int(d[9]), int(d[8]), int(d[11]), int(d[10])))
    fp.close()

def save_pulse_csv(filename, data):
    print('Saving file:', filename)
    fp = open(filename, 'w')
    fp.write('  TIMESTAMP,       COUNTER, AVG RATE, INST RATE\n')
    for d in data:
        fp.write('%1s%10d, %13.3f, %8.3f, %9.3f\n' % (d[-1], int(d[0]), round(float(d[1]), 3), round(float(d[2]), 3), round(float(d[3]), 3)))
    fp.close()

def load_meters(dir, meters):
    #loc = pytz.timezone('America/Vancouver')
    loc = pytz.timezone('UTC')

    # load all power meter CSV files into memory
    raw_data = []
    for meter in meters:
        filename = '%s/%s.csv' % (dir, meter)
        raw_data.append(load_csv(filename))

    # index by timestamp each row to have a timestamp of 0 seconds
    print('Fixing timestamps, indexing by timestamp...')
    row_pointers = [[[] for j in range(len(meters))] for i in range(minute_len)]
    for i, meter in enumerate(meters):
        for j, row in enumerate(raw_data[i]):
            #raw_ts = int(row[0])
            dt = loc.localize(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'))
            raw_ts = dt.timestamp()
            if not (start_ts <= raw_ts <= end_ts):
                #print('Raw TS', raw_ts, 'out of range', start_ts, 'to', end_ts)
                continue
            tick = int((raw_ts - start_ts) / 60)
            #ts = start_ts + minute_tick * 60
            row_pointers[tick][i].append(row[1:])
        raw_data[i] = []
        
    return row_pointers
    
rawdata_dir = 'dump'
output_dir = 'public'
min_per_year = 525600 # 1 year in minutes
years = 2
minute_len = int(min_per_year * years)
start_ts = 1333263600
end_ts = 1333263600 + (minute_len - 1) * 60
solutions = ['1 missing', 'lots missing', 'mulit-rec', 'I resum -amt', 'P resum -amt', 'Q resum -amt', 'S resum -amt', 'got zero', 'counter reset']
issues = [0 for i in range(len(solutions))]

power_meters = ['WHE', 'RSE', 'B1E', 'B2E', 'BME', 'CDE', 'CWE', 'DNE', 'DWE', 'EBE', 'EQE', 'FGE', 'FRE', 'GRE', 'HPE', 'HTE', 'OFE', 'OUE', 'TVE', 'UTE', 'WOE']
water_gas_meters = ['WHW', 'HTW', 'WHG', 'FRG']
       
# report incomplete resords and fix for power
print()
print('*** Fixing power data and report incomplete resords...')
power_data = load_meters(rawdata_dir, power_meters)
print('Timestamp  | %s | TL' % ' '.join(power_meters))
for tick in range(minute_len):
    ts = start_ts + tick * 60
    counts = []
    incomplete = 0
    over1 = False
    got0 = False
    _v = 0.0
    _i = 0.0
    _f = 0.00
    _dpf = 0.00
    _apf = 0.00
    _p = 0
    _pt = 0
    _q = 0
    _qt = 0
    _s = 0
    _st = 0
    
    for i, power_meter in enumerate(power_meters):        
        if power_meter == 'UNE':
            continue

        value = len(power_data[tick][i])

        if value < 1:
            incomplete += 1
            value = '  -'
            power_data[tick][i].append(power_data[tick - 1][i][0][:])
            power_data[tick][i][0][6] = '0'
            power_data[tick][i][0][8] = '0'
            power_data[tick][i][0][10] = '0'
            power_data[tick][i][0][-1] = '+'
        else:
            if float(power_data[tick][i][0][1]) == 0.0:
                got0 = True
                value = '  0'
            else:
                if value > 1:
                    over1 = True
                value = '%3d' % value 
            power_data[tick][i][0].append(' ')
            
            if tick > 0 and power_data[tick - 1][i][0][-1] == '+':
                hist = 0
                for hist in range(tick - 1, 0, -1):
                    if power_data[hist][i][0][-1] == ' ':
                        break;
                diff = tick - hist
                if 1 < diff < 10:
                    _pt = (int(power_data[tick][i][0][6]) - int(power_data[hist][i][0][6])) / diff
                    _qt = (int(power_data[tick][i][0][8]) - int(power_data[hist][i][0][8])) / diff
                    _st = (int(power_data[tick][i][0][10]) - int(power_data[hist][i][0][10])) / diff
                    
                    for j in range(1, diff):
                        power_data[hist + j][i][0][6] = str(int(power_data[hist][i][0][6]) + int(_pt) * j)
                        power_data[hist + j][i][0][8] = str(int(power_data[hist][i][0][8]) + int(_qt) * j)
                        power_data[hist + j][i][0][10] = str(int(power_data[hist][i][0][10]) + int(_st) * j)

        power_data[tick][i][0][0] = str(ts)
        if i == 0:
            _v = float(power_data[tick][i][0][1])
            _i = float(power_data[tick][i][0][2])
            _f = float(power_data[tick][i][0][3])
            _dpf = float(power_data[tick][i][0][4])
            _apf =float(power_data[tick][i][0][5])
            _p = int(power_data[tick][i][0][7])
            _pt = int(power_data[tick][i][0][6])
            _q = int(power_data[tick][i][0][9])
            _qt = int(power_data[tick][i][0][8])
            _s = int(power_data[tick][i][0][11])
            _st = int(power_data[tick][i][0][10])
        else:
            _i -= float(power_data[tick][i][0][2])
            _p -= int(power_data[tick][i][0][7])
            _q -= int(power_data[tick][i][0][9])
            _s -= int(power_data[tick][i][0][11])

        counts.append(value)
    
    new_agg = old_agg = float(power_data[tick][0][0][2])

    if _i < 0.0:
        issues[3] += 1
        power_data[tick][0][0][2] = str(round(float(power_data[tick][0][0][2]) - _i, 1));
        new_agg = float(power_data[tick][0][0][2])
     
    if _p < 0.0:
        issues[4] += 1
        power_data[tick][0][0][7] = str(int(power_data[tick][0][0][7]) - _p);

    if _q < 0.0:
        issues[5] += 1
        power_data[tick][0][0][9] = str(int(power_data[tick][0][0][9]) - _q);

    if _s < 0.0:
        issues[6] += 1
        power_data[tick][0][0][11] = str(int(power_data[tick][0][0][11]) - _s);

    if incomplete > 0 or over1 or got0 or _i < 0.0:
        if incomplete == 1:
            issues[0] += 1
        elif incomplete > 1:
            issues[1] += 1
        
        if got0:
            issues[7] += 1

        if over1:
            issues[2] += 1

        print('%10d | %s | %2d | ' % (ts, ' '.join(counts), incomplete), end = '')
        
        if old_agg == new_agg:
            print()
        else:
            print('%5.1fA -> %5.1fA' % (old_agg, new_agg))
        
# save all power meter data to CSV files
for i, power_meter in enumerate(power_meters):
    filename = '%s/%s.csv' % (output_dir, power_meter)
    save_power_csv(filename, [j[i][0] for j in power_data])
power_data = []
print()

print()
print('Issues Tally:')
for i in range(len(solutions)):
    print('%-32s = %7d' % ('   ' + solutions[i], issues[i]))
print('%-32s = %7d / %7d, %3.1f%% errors' % ('Total Issues', sum(issues[:2]), minute_len, float(sum(issues[:2])) / float(minute_len)))
print()

# report incomplete resords and fix for water and gas
print()
print('*** Fixing water and gas data and report incomplete resords...')
water_gas_data = load_meters(rawdata_dir, water_gas_meters)
print('Timestamp  | %s | TL' % ' '.join(water_gas_meters))
for tick in range(minute_len):
    ts = start_ts + tick * 60
    counts = []
    incomplete = 0
    over1 = False
    got0 = False
    rest = False
    
    for i, meter in enumerate(water_gas_meters):        
        value = len(water_gas_data[tick][i])

        if value < 1:
            incomplete += 1
            value = '  -'
            water_gas_data[tick][i].append(water_gas_data[tick - 1][i][0][:])
            water_gas_data[tick][i][0][-1] = '+'
        else:
            if float(water_gas_data[tick][i][0][1]) == 0.0:
                got0 = True
                value = '  0'
            else:
                if value > 1:
                    over1 = True
                value = '%3d' % value 
            water_gas_data[tick][i][0].append(' ')
        
        # reset between ts = 1342287780 and 1342310580
        if tick > 0 and float(water_gas_data[tick - 1][i][0][1]) > float(water_gas_data[tick][i][0][1]): 
            rest = True

        water_gas_data[tick][i][0][0] = str(ts)
        counts.append(value)

    if incomplete > 0 or over1 or got0 or rest:        
        if incomplete == 1:
            issues[0] += 1
        elif incomplete > 1:
            issues[1] += 1
        
        if got0:
            issues[7] += 1

        if over1:
            issues[2] += 1
            
        if rest < 0.0:
            issues[8] += 1

        print('%10d | %s | %2d | %s' % (ts, ' '.join(counts), incomplete, 'rest!' if rest else ''))

print('Fixing any resets...')
offset = [0.0 for i in water_gas_meters]
for tick in range(1, minute_len):
    ts = start_ts + tick * 60

    for i, meter in enumerate(water_gas_meters):        
        diff = 0.0
        if float(water_gas_data[tick - 1][i][0][1]) > float(water_gas_data[tick][i][0][1]): 
            diff = float(math.ceil(float(water_gas_data[tick - 1][i][0][1]))) - float(water_gas_data[tick - 1][i][0][1])
            print('\t', meter, 'RESET:', water_gas_data[tick - 1][i][0], ' > ', water_gas_data[tick][i][0])
        else:
            diff = float(water_gas_data[tick][i][0][1]) - float(water_gas_data[tick - 1][i][0][1])
            
        water_gas_data[tick - 1][i][0][1] = str(offset[i])
        offset[i] += diff
        
for i, meter in enumerate(water_gas_meters):        
    water_gas_data[-1][i][0][1] = str(offset[i])
        
# save all power meter data to CSV files
for i, meter in enumerate(water_gas_meters):
    filename = '%s/%s.csv' % (output_dir, meter)
    save_pulse_csv(filename, [j[i][0] for j in water_gas_data])
water_gas_data = []
print()

        
print()
print('Issues Tally:')
for i in range(len(solutions)):
    print('%-32s = %7d' % ('   ' + solutions[i], issues[i]))
print('%-32s = %7d / %7d, %3.1f%% errors' % ('Total Issues', sum(issues[:2]), minute_len, float(sum(issues[:2])) / float(minute_len)))

    
