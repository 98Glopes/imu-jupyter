# -*- coding: utf-8 -*-
##################################################################################################################
# Platform for study of IMU features and functionality (using Samsung S3 internal phone IMU) 
# Demo program (imu.py)
#
# Copyright (c) 2014 Bernard Chan 
# chanlhock@gmail.com
#
# Date			Author          Notes
# 04/09/2014	     Bernard Chan   Initial release
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation; either version 2.1 of the License, or (at your
# option) any later version.
##################################################################################################################
# This program is tested to run on Windows based Python 3.4.1 and Pygame 1.9.2
# Pygame 1.9.2 installation (pygame‑1.9.2a0.win32‑py3.4.exe) for Windows can be found at:
# http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame

# Code included leveraged from open source with thanks :-) are:
#    Python code:
#       ponycube.py, euclid.py
#    C code to be compiled into modules to be called from Python:
#       MadgwickAHRS.c & MadgwickAHRS.h compiled by gcc to MadgwickAHRS.pyd 
#       gcc -shared -IC:\Python34\include -LC:\Python34\libs MadgwickAHRS.c -lpython34 -o MadgwickAHRS.pyd 

# IMU+GPS-Stream apps (install to mobile phone through Google PlayStore)
# - sends the measurements from your phone inertial sensors via UDP as CSV (Comma-Separated Values) 
#   to a computer in your network.
# This turns your phone into a wireless inertial measurement unit (IMU).
# The following sensors are supported:
# - Accelerometer
# - Gyroscope
# - Magnetometer
# If your phone has not all these sensors, only the available sensor data is transmitted.
# Example UDP packet:
# 890.71558, 3, 0.076, 9.809, 0.565, 4, -0.559, 0.032, -0.134, 5, -21.660,-36.960,-28.140
# Timestamp [sec], sensorid, x, y, z, sensorid, x, y, z, sensorid, x, y, z
# Sensor id:
# 3 - Accelerometer (m/s^2)
# 4 - Gyroscope (rad/s)
# 5 - Magnetometer (micro-Tesla uT)
##################################################################################################################

#### include external libraries ####
import socket
import traceback
import csv
import struct
import sys, time, string, math
from MadgwickAHRS import *
import os

#### assign local variables ####
host = '192.168.43.145'
port = 5555
csvf = 'accelerometer.csv'

#### do UDP stuff (communicate with mobile phone's WiFi) ####
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))

first_timestamp = 0
first_rads = 0
first_angle = 0
atual_timestamp = 0
atual_rads = 0
atual_angle = 0

message, adress = s.recvfrom(8192)
message = message.decode('UTF-8').split(', ')
first_timestamp = float(message[0])

while True:

    message, address = s.recvfrom(8192)
    message = message.decode('UTF-8').split(', ')

    if len(message) < 9: continue

    atual_rads = float(message[8])
    atual_timestamp = float(message[0])

    dt = atual_timestamp - first_timestamp
    atual_angle = atual_angle + atual_rads*dt

    print('Angular speed: ',first_rads)
    print('dt: ', dt)
    print('Angle: ', math.degrees(atual_angle))

    first_angle = atual_angle
    first_rads = atual_rads
    first_timestamp = atual_timestamp
    #os.system('clear')

    