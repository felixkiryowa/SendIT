
[![Build Status](https://travis-ci.org/felixkiryowa/SendIT.svg?branch=develop)](https://travis-ci.org/felixkiryowa/SendIT)

[![Maintainability](https://api.codeclimate.com/v1/badges/83fbc29f2b74f182296d/maintainability)](https://codeclimate.com/github/felixkiryowa/SendIT/maintainability)

[![Coverage Status](https://coveralls.io/repos/github/felixkiryowa/SendIT/badge.svg?branch=develop)](https://coveralls.io/github/felixkiryowa/SendIT?branch=develop)


#  SendIT API Endpoints
 SendIT is a courier service that helps users deliver parcels to different destinations. SendIT  provides courier quotes based on weight categories.

# Features Required

- Users can create an account and log in.  
- Users can create a parcel delivery order.  
- Users can change the destination of a parcel delivery order.  
- Users can cancel a parcel delivery order.  
- Users can see the details of a delivery order. 
- Admin can change the ​status​​ and ​present​​ ​location​​ of a parcel delivery order. 

### Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites for API

Things you need to install for the API to work

* Python
### Installing

To deploy this application follow these steps;
* clone/download this project from git hub
```
 git clone https://github.com/felixkiryowa/SendIT.git

```
* Extract the project and open it in an Editor for example visual studio code ,Pycharm or any editor of your choice.
* create a python virtual environment using the following command
```
 virtualenv  env 

``` 
* In windows, navigate to scripts in the env folder where the virtual environment exists.
```
 cd venv\scripts

```
*  Activate the virtual environment using the following command ;
```
activate

```
* In linux, activate the virtual environment using ;
```
source env/Scripts/activate

```
* After Activating the virtual environment Execute the application by running a a given command

```
 python run.py

``` 

* After running that command the server will start running at http://127.0.0.1:5000/ which is the default URI 

* use the endpoints given below to test the api using postman, which is the highly recommended app to use when testing api's.

* This is the link to my postman collection https://documenter.getpostman.com/view/5384614/RWgxuawi

### Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST     |  /auth/signup  | Register a user 
POST     |  /auth/login   | Login a user
PUT      |  /parcels/<parcel_id>/destination | Change the location  of a specific parcel  delivery order 
PUT      |  /parcels/<parcel_id>/status  |  Change the status of  a specific parcel  delivery order 
PUT     |   /parcels/<parcel_id>/presentlocation | Change the present  location of a specific  parcel delivery order

## Testing 

Tests can be run after by installing pytest using the command below ;
```
 pip install pytest

```

Then after installing pytest, type the command below to run the tests in the project directory
```
 pytest

```
You can also get the test coverage though this requires you to have installed pytest --cov by running the command below.
```
pip install pytest-cov
```
To get the test coverage, you type the command below.
```
 pytest --cov .
```
### Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python.
* [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create isolated Python environments
* [PIP](https://pip.pypa.io/en/stable/) - Python package installer.


### Deployment

The API is hosted on [Heroku](https://francissendit.herokuapp.com/api/v2/parcels).

## Authors
- [felixkiryowa](https://github.com/felixkiryowa/)

## Contact me 
- Email:franciskiryowa68@gmail.com
- Phone Number:+256700162509
- Address:Lubaga

