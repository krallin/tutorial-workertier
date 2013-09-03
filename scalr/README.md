Configuration Parameters (Global Variables)
===========================================

Roles
=====

  + `WORKERTIER_CONFIG`: Path to the config file (e.g. `/etc/workertier.ini`)
  + `WORKERTIER_ROLE`: `consumer` or `web`

Farm
====

  + `MEMCACHED_HOST`: DNS entry mapped to Memcached (Only for nonstandard
    DNS-based Cache)
  + `MEMCACHED_PORT`: Port for Memcached (11211)
  + `MEMCACHED_TIMEOUT`: Connection timeout for Memcached (e.g. 2)
  + `RABBIT_HOST`: DNS entry mapped to RabbitMQ
  + `RABBIT_PORT`: Port for RabbitMQ (5672)
  + `RABBIT_USERNAME`: Arbitrary username for RabbitMQ
  + `RABBIT_PASSWORD`: Arbitrary password for RabbitMQ
  + `RABBIT_QUEUE`: Arbitrary queue name for RabbitMQ
  + `RABBIT_VHOST`: Arbitrary virtualhost for RabbitMQ
