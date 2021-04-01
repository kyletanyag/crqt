#!/bin/bash

# will update cve search db
service redis-server start
cd ./dms/cve_search
python3 ./sbin/db_updater.py -v