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




## Deployment
The website is (not automatically) deployed to railway. If you need an update there just ask Thibaut.

(also not putting the public link here for reasons)
