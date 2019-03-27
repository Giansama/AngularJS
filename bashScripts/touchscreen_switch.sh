#!/bin/bash
touch_id=$(xinput list | grep Touch | cut -d = -f 2 | cut -f 1)
touchscreen_status=$(xinput list-props $touch_id | grep "Device Enabled" | tail -c 2)
if(( $touchscreen_status == "0" )); then
    xinput enable $touch_id 
else
    xinput disable $touch_id
fi
