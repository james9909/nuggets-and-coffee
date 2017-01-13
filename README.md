# nuggets-and-coffee

*Nuggets and Coffee* is a website designed for both coffee and chicken nugget enthusiasts. Users will be able to look up where to buy either coffee or nuggets, search for different recipes, and discuss their favorite food with other fans.

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
