SET GLOBAL time_zone = 'UTC';
SET time_zone = 'America/Vancouver';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'M_E' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/WHE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'RSE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/RSE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'B1E' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/B1E.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'B2E' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/B2E.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'BME' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/BME.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'CDE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/CDE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'CWE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/CWE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'DNE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/DNE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'DWE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/DWE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'EBE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/EBE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'EQE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/EQE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'FGE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/FGE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'FRE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/FRE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'GRE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/GRE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'HPE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/HPE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'HTE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/HTE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'OFE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/OFE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'OUE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/OUE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'TVE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/TVE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'UTE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/UTE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'WOE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/WOE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';


SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'CTE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/CTE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'LIE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/LIE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, v, a, freq, pf_displ, pf_va, wh, w, varh, var, vah, va FROM meter_power WHERE home_id = 'MAK' AND meter_id = 'MWE' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/MWE.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';


SELECT UNIX_TIMESTAMP(read_dt), read_dt, pulses, avg_rate, inst_rate FROM meter_pulse WHERE home_id = 'MAK' AND meter_id = 'M_W' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/WHW.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, pulses, avg_rate, inst_rate FROM meter_pulse WHERE home_id = 'MAK' AND meter_id = 'HTW' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/HTW.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, pulses, avg_rate, inst_rate FROM meter_pulse WHERE home_id = 'MAK' AND meter_id = 'M_G' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/WHG.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

SELECT UNIX_TIMESTAMP(read_dt), read_dt, pulses, avg_rate, inst_rate FROM meter_pulse WHERE home_id = 'MAK' AND meter_id = 'FRG' ORDER BY home_id, meter_id, read_dt
INTO OUTFILE './dump/FRG.csv' FIELDS ENCLOSED BY '' TERMINATED BY ',' ESCAPED BY '' LINES TERMINATED BY '\n';

