#!/bin/sh

newrelic-admin run-program 
# python3 db_init.py

exec "$@"