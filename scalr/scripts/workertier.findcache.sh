#!/bin/bash
# NOTE: This script MUST RUN as async
# NOTE: This script should run LAST in your HostUp chain
set -o nounset
set -o errexit

sleep 5 # Huge hack to give IpListBuilder time to run

PIDFILE=/var/run/workertier.*.pid
kill -s USR1 `cat $PIDFILE`
