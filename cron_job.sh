#!/bin/bash
#run in background as ./cron_job.sh &

while true
do
	./epscript.sh
	sleep 300
done
