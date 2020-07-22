#!/usr/bin/env python

import time
import subprocess

ORIENTATIONS = ['normal','inverted','left','right']
PREV_STATE = -1

BUFFER = 10

DEVICE_INFO = {
    "screen": "eDP1",
    "touchscreen": "Raydium Corporation Raydium Touch System",
    "touchpad": "Synaptics TM3201-001",
    "keyboard": "AT Translated Set 2 keyboard"
}

DISABLE_KB = True

ORIENTATION_CMD = 'xrandr'
ORIENTATION_RE = ''

TRANSFORMATION_MATRIX = {
    "normal": "1 0 0 0 1 0 0 0 1",
    "left": "0 -1 1 1 0 0 0 0 1",
    "right": "0 1 0 -1 0 1 0 0 1",
    "inverted": "-1 0 1 0 -1 1 0 0 1"
}

def doRotate(orientation):
    rotateScreenCmd = "xrandr --output {} --rotate {}".format(
        DEVICE_INFO['screen'],
        orientation)
    rotateTouchCmd = "xinput --set-prop '{}' --type=float 'Coordinate Transformation Matrix' {}".format(
        DEVICE_INFO['touchscreen'],
        TRANSFORMATION_MATRIX[orientation])

    toggleKbCmd = ""
    if DISABLE_KB == True:
        setCmd = "xinput --enable" if orientation == 'normal' else "xinput --disable"
        toggleKbCmd = "{} '{}'; {} '{}'".format(
            setCmd,
            DEVICE_INFO['touchpad'],
            setCmd,
            DEVICE_INFO['keyboard'])

    res = subprocess.call("{}; {}; {}".format(rotateScreenCmd,rotateTouchCmd,toggleKbCmd), shell=True)

while True:
    angleX = int(subprocess.check_output(
        "cat /sys/bus/iio/devices/iio:device*/in_incli_x_raw", shell=True))
    angleY = int(subprocess.check_output(
        "cat /sys/bus/iio/devices/iio:device*/in_incli_y_raw", shell=True))

    if abs(angleY) < abs(angleX) - BUFFER:
        if angleX >= 0:
            state = 0
        else:
            state = 1

    if abs(angleY) > abs(angleX) + BUFFER:
        if angleY >= 0:
            state = 2
        else:
            state = 3

    if state != PREV_STATE:
        doRotate(ORIENTATIONS[state])

    PREV_STATE = state
    time.sleep(1)