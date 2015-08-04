mount /dev/sdb1 /media/usbkey
mysql -u root -p smarthome < export.sql
rm dump/*
mv /var/lib/mysql/*.csv dump/
cd dump/
chown root:root *.csv
tar -czvf meters.tar.gz *.csv
mv meters.tar.gz /media/usbkey
umount /media/usbkey
cd 
