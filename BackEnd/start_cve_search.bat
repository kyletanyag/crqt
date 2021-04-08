@ECHO OFF
ECHO Starting up CVE Search Server
ECHO Make sure to start redis server in WSL
python %~dp0\DMS\cve_search\web\index.py