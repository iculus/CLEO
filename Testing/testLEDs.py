#!/usr/bin/python
# this program takes no input and outputs test patterns to the microcontroller with leds attached

import sys
sys.path.insert(0,'/home/admin/CLEO/Setup/')

from setup import *
from SensorSetup import getPort

print LEDComputer

print getPort(LEDComputer)
