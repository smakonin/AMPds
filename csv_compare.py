#!/usr/bin/env python3
#
#    A utility to compare the rows of a CSV file ignoring whitespace (csv_compare.py)
#
#    Copyright (C) 2015 Stephen Makonin. All Right Reserved.
#

import os, sys, csv, ast
      
if len(sys.argv) != 3:
    print()
    print('USAGE: %s [file1.csv] [file2.csv]' % (sys.argv[0]))
    print()
    exit(1)

filename1 = sys.argv[1]
fp1 = open(filename1, 'r')
csv1 = csv.reader(fp1)

filename2 = sys.argv[2]
fp2 = open(filename2, 'r')
csv2 = csv.reader(fp2)

print()
print('Comparing %s and %s...' % (filename1, filename2))
print()

count = 0
diff = 0
eof1 = False
eof2 = False
next(csv1) # skip the header compare
next(csv2)
while not eof1 and not eof2:
    
    try:
        row1 = next(csv1)
    except:
        eof1 = True
    row1 = [ast.literal_eval(v.strip()) for v in row1]
        
    try:
        row2 = next(csv2)
    except:
        eof2 = True
    row2 = [ast.literal_eval(v.strip()) for v in row2]

    if eof2 or eof2:
        continue

    if row1 != row2:
        diff += 1
        print('Rows/lines %d are not the same:' % count)
        print('   ', row1)
        print('   ', row2)
        print()        
        
    count += 1

fp1.close()
fp2.close()  

if eof1 and not eof2:
    print('ERROR: file %s is shorter than %s!' % (filename1, filename2))
    
if not eof1 and eof2:
    print('ERROR: file %s is shorter than %s!' % (filename2, filename1))

print('Found %d differences in %d rows or %s%%.' % (diff, count, str(round(diff / count * 100, 1))))
print()
print('DONE!')
print()
