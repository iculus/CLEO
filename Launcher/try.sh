#!/bin/sh

export DISPLAY=:0.0
xhost +

/usr/bin/python /home/admin/CLEO/Launcher/launch.py >/home/admin/CLEO/Launcher/p.out 2>&1 &
#/home/admin/ngrok tcp 22 -remote-addr=1.tcp.ngrok.io:27102 &
#/usr/bin/python /home/admin/CLEO/ReadSensors/read.py &
#/usr/bin/python /home/admin/CLEO/Lights/lightMessage2.py &
#/usr/bin/python /home/admin/CLEO/Leap/leapController.py &

exit 0
