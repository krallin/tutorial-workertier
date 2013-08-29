#!/bin/bash
set -o nounset
set -o errexit

cat << EOF > $WORKERTIER_CONFIG 
[cache]
class=workertier.backends.cache.memcached.MemcachedCache
host=$MEMCACHED_HOST
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
