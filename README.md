# nuggets-and-coffee

*Nuggets and Coffee* is a website designed for both coffee and chicken nugget enthusiasts. Users will be able to look up where to buy either coffee or nuggets, search for different recipes, and discuss their favorite food with other fans.

## Introduction

[Watch our demo here](https://youtu.be/3xrn0bD6Pco)

Team Members
- James Wang - Project Manager
- Jiaqi Gao - UI/UX
- Sharon Lin - Backend/Recipes
- Jordan Yaqoob - Database management

## Setting up
Install all required python libraries by running:

`$ pip install -r requirements.txt`

API keys must be placed in a file called `.keys`, located in the root directory of the project. Each key needs to be placed on a new line, following the format `KEY=VALUE`. No quotes are necessary

Example:
```
KEY=VALUE
API_KEY=SECRET
```

An example config can be found in `utils/.keys.example`

## Running the application

In the root directory of the repository, run:
```
$ python app.py
```
Open [localhost:5000](http://localhost:5000) in a browser

## APIs

* Foursquare: Provides a list of places that sell a certain food item. Used for finding the nearest places to buy coffee/chicken nuggets
* Google Maps: Allows us to render a map at any given coordinates. Used for displaying locations.
* Food2Fork: Allows us to search for recipes containing a given ingredient. Used for our recipe search functionality.
* Geocoder: Allows us to get the latitude and longitude of a given address. Used in conjunction with the Google Maps api to display locations.
