#!/bin/bash
powerbutton_id=$(xinput list | grep Power | cut -d = -f 2 | cut -f 1 | tail -n 1)
powerbutton_status=$(xinput list-props $powerbutton_id | grep "Device Enabled" | tail -c 2)
if(( $powerbutton_status == "0" )); then
    xinput enable $powerbutton_id
else
    xinput disable $powerbutton_id
fi
