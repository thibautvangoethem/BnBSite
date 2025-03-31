# New and improved BnB site

![BnB helper site](logo.ico)

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Developing](#developing)
- [Deployment](#Deployment)

## Introduction

Bnb site, making our life a litle bit easier. Rolling 6000 dice all at once, no longer having to wait an hour on Jim.
[WIP]

## Installation
Easiest way to get everything up and running is using docker-compose.
Simply run "docker-compose up --build" in the root and all 3 containers shoudl start up and be linked.
These containers are:
- Postgresql alpine image 
- Backend python container
- Frontend react app

This logically requires docker (and wsl2 + docker hub on windows)

To run without docker, look at [developing](#developing)

## developing
### requirements
- [Python](https://www.python.org/downloads/) (I develop in 3.11, others could possibly work too)
- [npm & node](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
- [postgresql](https://www.postgresql.org/)
- [vscode](https://code.visualstudio.com/)

**note: installation guide for windows, linux possible given some changes**

### setup postgresql
for local development I have place the db env variable in the launch.json => it is "postgresql+psycopg2://postgres:postgres@localhost:5432/bnbsite"

So for postgres all we need is a single database on the default user, and name it "bnbsite"

- download and install postgres from the above website (make sure it is added to your path)
- open a command line window
- Run  "psql -U postgres" => fill in the default password "postgres"
    - you should now see "postgres=#" in front of your text
- create the database with "CREATE DATABASE bnbsite"
- (tables will be create later on by python)

**optional**
You might need to end up deleting your database quite a bit, so a database viewer app would be nice. (I use dbeaver, but there are also postgresql extensions)

### setup python
- open up a cmd in the root of the project (same folder with .vscode, backend, and frontend)
- Create a venv "python -m venv .venv"
- Activate the venv ".venv\Scripts\activate.bat" 
- Install requirements.txt "pip install -r backend\requirements.txt"
    - oeps pip freeze heeft mijn global python env gedumped, dus daar staan te veel reqs in
- Test validity by running the backend "py backend\main.py"
    - yes it should crash because it doesnt find the db string

### setup frontend
- open up a cmd in the frontend folder
- install dependencies "npm install"
    - yes there are vulnerabilites, I love javascript
- Test validity by running "npm run start"

### setup vscode
- Simply open the root folder in vscode
- You should be prompted to install some extensions, click yes
    - No errors should pop up
- Tasks have been set up to run everything
    - Go to the play+bug submenu at the right in vscode
- run the "Run frontend & backend" task
    - this starts up:
         - The python backend in debug with db env variable(same as run backend task)
         - The npm frontend in debug (same as run frontend task)



## Deployment
The website is (not automatically) deployed to railway. If you need an update there just ask Thibaut.

(also not putting the public link here for reasons)
