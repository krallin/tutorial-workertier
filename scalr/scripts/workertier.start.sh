#!/bin/bash
set -o nounset
set -o errexit

workertier --daemon --config "$WORKERTIER_CONFIG" "$WORKERTIER_ROLE"
