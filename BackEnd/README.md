# Flask Tutorial Notes:
Tutorial: https://www.youtube.com/watch?v=Urx8Kj00zsI&list=WL&index=32&t=133s

## 1. Must install pipenv first:
 ```
$ pip install pipenv
```
Resource on [pipenv](https://realpython.com/pipenv-guide/).

From what I gather, it seem it is used to build pip libs so other executables do not interfear

## 2. Install Flask, Flask sqlalchemy, Flask-CORS
```
$ pipenv install flask flask-sqlalchemy flask-cors
```

## 3. To export variables in Windows use 'set' command in cmd
```
set FLASK_APP=BackEnd
set FLASK_DEBUG=1
```

## 4. Downloaded and installed postman to monitor API
Can be downloaded [here](https://www.postman.com/downloads/).


## Note: Future Improvements for security:
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https



# How to Run
```
$ pip install pipenv
$ pipenv install flask flask-sqlalchemy flask-cors
$ pipenv shell
$ set FLASK_APP=BackEnd
$ set FLASK_DEBUG=1
$ flask run
```