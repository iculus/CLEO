#!/bin/sh

var=`grep 'password' /home/admin/setup.CLEO | awk '{split($0,a,"=");print a[2]}'`

#password
echo $var | sudo -S python /home/admin/CLEO/Connect/connectionManager.py $1 $2

$SHELL


