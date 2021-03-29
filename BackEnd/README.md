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


# How to Run CVE-Search
IMPORTANT: please follow the prior guide for flask first before running cve-search

Prerequisites:
Ubuntu Subsystem for Windows - https://docs.microsoft.com/en-us/windows/wsl/install-win10
Window Terminal - https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701?activetab=pivot:overviewtab
Install Mongo Windows Service - https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/#run-mongodb-from-cmd
git installed on windows
Python installed on windows with pip


On Windows CMD create and clone CVE Search repo: 
```
> mkdir cve_search && cd cve_search
> git clone https://github.com/cve-search/cve-search.git .
```

On Ubuntu Terminal open cve_search directory and run the following commands:
```
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo apt-get install redis-server
$ sudo apt-get install redis-server
$ pip3 install flask flask-pymongo
$ sudo service redis-server start
```

In same terminal download cve data: 
```
$ python3 ./sbin/db_mgmt_cpe_dictionary.py -p
$ python3 ./sbin/db_mgmt_json.py -p
$ python3 ./sbin/db_updater.py -c # This will take >45minutes on a decent machine,please be patient
```

In new windows CMD start flask web server:
```
> pip3 install flask flask-pymongo
> python .\web\index.py # this will start flask server on port 5000
```

In ubuntu terminal, test web server:
```
$ curl http://127.0.0.1:5000/api/browse/zyxel
$ curl http://127.0.0.1:5000/api/cve/CVE-2010-3333
$ curl http://127.0.0.1:5000/api/search/zyxel/p-660hw
```

## To run server:
In Ubuntu Terminal:
```
$ sudo service redis-server start
```

In Windows CMD:
```
> cd <path>\cve_search
> python .\web\index.py # this will start flask server on port 5000
```

## Updating Databases

