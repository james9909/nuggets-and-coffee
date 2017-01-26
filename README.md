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
