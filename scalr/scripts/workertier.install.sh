#!/bin/bash
set -o nounset
set -o errexit

apt-get install -y python-gevent
apt-get install -y python-pip
pip install workertier
