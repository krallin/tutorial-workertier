#!/bin/bash
set -o errexit
set -o nounset

# We will accept a fail on all those commands.
rabbitmqctl add_vhost $RABBIT_VHOST  || true  # We don't care if this already exists
rabbitmqctl add_user $RABBIT_USERNAME $RABBIT_PASSWORD || rabbitmqctl change_password $RABBIT_USERNAME $RABBIT_PASSWORD
rabbitmqctl set_permissions -p $RABBIT_VHOST $RABBIT_USER ".*" ".*" ".*"
