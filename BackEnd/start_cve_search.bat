@ECHO OFF
ECHO Starting up CVE Search Server
ECHO Make sure to start redis server in WSL
ECHO sudo service redis-server start
python %~dp0\DMS\cve_search\web\index.py