# Travis

[![Build Status](https://travis-ci.org/felixkiryowa/SendIT.svg?branch=develop)](https://travis-ci.org/felixkiryowa/SendIT)

# Maintainability

[![Maintainability](https://api.codeclimate.com/v1/badges/83fbc29f2b74f182296d/maintainability)](https://codeclimate.com/github/felixkiryowa/SendIT/maintainability)

# Coverage
[![Coverage Status](https://coveralls.io/repos/github/felixkiryowa/SendIT/badge.svg?branch=develop)](https://coveralls.io/github/felixkiryowa/SendIT?branch=develop)

#  SendIT API Endpoints
 SendIT is a aparcel delivery website for SendIT company dealing in delivering different parcel as orders from their customers.

# Features Required

- Create a parcel delivery order
- Get all parcel delivery orders
- Get a specific parcel delivery order
- Cancel a parcel delivery order

### Getting Started

Clone the project using this link to review [link](https://github.com/felixkiryowa/SendIT.git).

### Installing

* Clone the project to your local machine
```
git clone https://github.com/felixkiryowa/SendIT.git
```

### Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
GET /parcels | Fetch all parcel delivery orders
GET /parcels/<parcelId> |  Fetch a specific parcel delivery order
GET /users/<userId> | parcels Fetch all parcel delivery orders by a specific user
PUT /parcels/<parcelId>/cancel | Cancel the specific parcel delivery order
POST /parcels | Create a parcel delivery order


### Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python.
* [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create isolated Python environments
* [PIP](https://pip.pypa.io/en/stable/) - Python package installer.


### Deployment

The API is hosted on [Heroku](https://francissendit.herokuapp.com/api/v1/parcels).

### Built With
[FLASK VIEWS](http://flask.pocoo.org/docs/1.0/views/) - Flask framework views 

## Authors
- [felixkiryowa](https://github.com/felixkiryowa/)

## Contact me 
- Email:franciskiryowa68@gmail.com
- Phone Number:+256700162509
- Address:Lubaga

