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


# How to Run Flask
```
$ <name of virtual env>/Scripts/activate # if virtual env not activated
$ set FLASK_APP=api
$ set FLASK_DEBUG=1
$ flask run
```
Port 5000 will have 


# Flask Tutorials:
https://www.youtube.com/watch?v=Urx8Kj00zsI&list=WL&index=32&t=133s
