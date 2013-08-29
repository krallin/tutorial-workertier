#!/bin/bash
set -o nounset
set -o errexit

PIDFILE=/var/run/workertier.$WORKERTIER_ROLE.pid
kill `cat $PIDFILE`
