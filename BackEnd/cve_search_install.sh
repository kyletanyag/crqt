#!/bin/bash
## This shell script will install cve search

apt-get update      # updates package list

# install packages
apt-get install -y python3
apt-get install -y python3-pip
apt-get install -y redis-server
pip3 install -r requirements.txt

# start redis server
service redis-server start

# populate CVE Search db
cd ./dms/cve_search/
python3 ./sbin/db_mgmt_cpe_dictionary.py -p
python3 ./sbin/db_mgmt_json.py -p
python3 ./sbin/db_updater.py -c # This will take >45minutes on a decent machine,please be patient


echo '======================FINISH INSTALL========================'
echo 'Create CMD window, and run web/index.py in cve_search'