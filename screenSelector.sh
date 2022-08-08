#!/bin/bash
while true
do
	/usr/bin/xrandr -q -display :0 | grep "connected" > /tmp/current-monitors.log 
	sleep 10
done
