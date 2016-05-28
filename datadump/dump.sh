#!/bin/bash

dumppath=/root/newdump
time=`date +%Y-%m-%d-%H%M`
zipname=dump-$time.zip


rm -rf $dumppath
mkdir -p $dumppath

psql -hceeb.c81wndto8oyq.us-east-1.rds.amazonaws.com -p8443 -Uceebbi -f /root/dump.sql -w -d ceeb

cd $dumppath
zip -e -P reENforceD -r /root/$zipname .
mv /root/$zipname /home/dumpuser/
chown dumpuser /home/dumpuser/$zipname
chmod 400 /home/dumpuser/$zipname
cd ..

rm -rf $dumppath
