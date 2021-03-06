#!/bin/bash
# NOTE: Only use this if you're using Scalarizr < 0.21.1
set -o nounset
set -o errexit

IPTABLES=/sbin/iptables
$IPTABLES --delete INPUT --protocol tcp --jump ACCEPT --source %event_internal_ip% --dport $MEMCACHED_PORT
$IPTABLES --delete INPUT --protocol tcp --jump ACCEPT --source %event_external_ip% --dport $MEMCACHED_PORT
