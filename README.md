# Cyber Resiliency Quantification Tool (CRQT)

### Before you Start
Make sure you have the following downloaded:
- [Node.js](https://nodejs.org/en/)


## Project setup Front-End
From this directory run
```
npm install
```
Note: The npm install command only has to be run once. This downloads all the needed packages for Vue to compile and serve the application. It will take a while to run the first time as it has to download packages.

### Compiles and hot-reloads for development
```
npm run serve
```
This will start the front-end application at http://localhost:8080/. The jmt.repo.api application will also need to be running for the application to work. (see above)


### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Devtools
Download the [Vue.js devtools Chrome Extension](https://chrome.google.com/webstore/detail/vuejs-devtools/ljjemllljcmogpfapbkkighbhhppjdbg) for debugging Vue.js applications in the browser.

## Project setup Back-End
From this directory run (Window cmd):
```
pip install pipenv
```
Note: pipenv is only compatible with Python 3.8. 
More information on pipenv: https://realpython.com/pipenv-guide/

### Run
From this directory run (Window cmd):
```
set FLASK_APP=BackEnd
set FLASK_DEBUG=1
flask run
```

Useful tool for testing backend: https://www.postman.com/downloads/

