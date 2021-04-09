# Running Flask

## 1. (optional) Install and Deploy Virtual Environment:
 ```
$ pip install virtualenv
$ virtualenv <name of virtual env> # I named mine backend_env
$ <name of virtual env>/Scripts/activate # activate virtual environment
```
Resource on [virtualenv](https://www.youtube.com/watch?v=N5vscPTWKOk).

From what I gather, it seem it is used to build pip libs so other executables do not interfear

Deactivate virtual environment
```
$ deactivate
```

## 2. Install Dependencies
```
$ pip install -r requirements.txt
```

## 3. To export variables in Windows use 'set' command in cmd
```
set FLASK_APP=api
set FLASK_DEBUG=1
```

## 4. Downloaded and installed postman to monitor API
Can be downloaded [here](https://www.postman.com/downloads/).


## Note: Future Improvements for security:
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https


## How to Run Flask
```
$ <name of virtual env>/Scripts/activate # if virtual env not activated
$ set FLASK_APP=api
$ set FLASK_DEBUG=1
$ flask run
```
Will be on Localhost:5000 


## Flask Tutorials:
https://www.youtube.com/watch?v=Urx8Kj00zsI&list=WL&index=32&t=133s


# CVE-Search
IMPORTANT: please follow the prior guide for flask first before running cve-search

## Prerequisites
Install Mongo Windows Service - https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/#run-mongodb-from-cmd

Python installed on windows with pip

### Installing Ubuntu 20.04 subsystem for Windows
To install Ubuntu 20.04 subsystem for Windows go to Window's Control Panel -> Programs and select Turn Windows features on or off. From there, check mark Windows Subsystem for Linux and press ok. After this, it will install subsystem functionality and require restart. After restart, goto Microsoft store and install Ubuntu 20.04. Once installed, open Ubuntu 20.04 so to put username and passwd for terminal. Once completed, you can open Ubuntu 20.04 in Windows Terminal and cd to CRQT directory.  

If problems occur during installation, please refer to https://docs.microsoft.com/en-us/windows/wsl/install-win10 or https://adamtheautomator.com/windows-subsystem-for-linux/ or https://www.youtube.com/watch?v=av0UQy6g2FA.

## Automatic Install
In Ubuntu Terminal run:
```
$ cd /mnt/<path_to_crqt>/BackEnd
$ chmod 700 ./cve_search_install.sh 
$ ./cve_search_install.sh
```

After install, proceed to run server section

## Manual Install
On Ubuntu Terminal open cve_search directory and run the following commands:
```
$ cd /mnt/<path_to_crqt>/BackEnd
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo apt-get install redis-server
$ pip3 install flask flask-pymongo
$ sudo service redis-server start
```

In same terminal download cve data: 
```
$ cd ./dms/cve_search/
$ python3 ./sbin/db_mgmt_cpe_dictionary.py -p
$ python3 ./sbin/db_mgmt_json.py -p
$ python3 ./sbin/db_updater.py -c # This will take >45minutes on a decent machine,please be patient
```

## To run server:
In Ubuntu Terminal:
```
$ sudo service redis-server start
```

In Windows CMD:
```
> cd <path_to_cqqt>\BackEnd\dms\cve_search
> python .\web\index.py # this will start flask server on port 2000
```

In ubuntu terminal, test web server:
```
$ curl http://127.0.0.1:2000/api/browse/zyxel
$ curl http://127.0.0.1:2000/api/cve/CVE-2010-3333
$ curl http://127.0.0.1:2000/api/search/zyxel/p-660hw
```

## Updating Databases
For repopulating db, in an Ubuntu terminal:
```
$ sudo service redis-server start
$ python3 ./sbin/db_updater.py -v -f
```

For updating without repopulating db, in an Ubuntu terminal:
```
$ sudo service redis-server start
$ python3 ./sbin/db_updater.py -v
```
