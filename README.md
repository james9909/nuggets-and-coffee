# nuggets-and-coffee

*Nuggets and Coffee* is a website designed for both coffee and chicken nugget enthusiasts. Users will be able to look up where to buy either coffee or nuggets, search for different recipes, and discuss their favorite food with other fans.

## Introduction

Our demo video is viewable at: https://youtu.be/3xrn0bD6Pco

Team Members
- James Wang - Project Manager
- Jiaqi Gao - UI/UX
- Sharon Lin - Backend/Recipes
- Jordan Yaqoob - Database management

## Setting up
The `foursquare` and `geocoder` python libraries are required to run the application, which can be installed using pip.

`$ pip install -r requirements.txt`

API keys must be placed in `utils/.keys`. Each key needs to be placed on a new line, following the format `KEY=VALUE`.

Example:
```
KEY=VALUE
API_KEY=SECRET
```

An example config can be found in `utils/.keys.example`

## Usage

To run the website from terminal:

- If flask is not installed
```
$ pip install flask
```
- If sqlite3 is not installed
```
$ pip install sqlite3
```
- If foursquare is not installed
```
$ pip install foursquare
```
- If geocoder is not installed
```
$ pip install geocoder
```
- To run from main directory
```
$ python app.py
```
- Open a browser to localhost:5000
