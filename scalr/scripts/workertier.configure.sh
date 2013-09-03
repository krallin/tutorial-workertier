#!/bin/bash
set -o nounset
set -o errexit

cat << EOF > $WORKERTIER_CONFIG 
[cache]
class=workertier.backends.cache.memcluster.scalr.ScalrMemcachedClusterCache
ip_list_home=/etc/scalr/private.d/hosts
memcached_role=memcached
refresh_signal=SIGUSR1
port=$MEMCACHED_PORT
timeout=$MEMCACHED_TIMEOUT

[dispatcher]
class=workertier.backends.dispatcher.rabbitmq.RabbitMQDispatcher
host=$RABBIT_HOST
port=$RABBIT_PORT
virtualhost=$RABBIT_VHOST
user=$RABBIT_USERNAME
password=$RABBIT_PASSWORD
queue=$RABBIT_QUEUE
EOF
