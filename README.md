# Travis

[![Build Status](https://travis-ci.org/felixkiryowa/SendIT.svg?branch=develop)](https://travis-ci.org/felixkiryowa/SendIT)

# Maintainability

[![Maintainability](https://api.codeclimate.com/v1/badges/83fbc29f2b74f182296d/maintainability)](https://codeclimate.com/github/felixkiryowa/SendIT/maintainability)

# Coverage
[![Coverage Status](https://coveralls.io/repos/github/felixkiryowa/SendIT/badge.svg?branch=develop)](https://coveralls.io/github/felixkiryowa/SendIT?branch=develop)

#  SendIT
 SendIT is a aparcel delivery website for SendIT company dealing in delivering different parcel as orders from their customers.

# Features
- Users can create an account and log in.
- Users can create a parcel delivery order.
- Users can change the destination of a parcel delivery p order.
- Users can cancel a parcel delivery order.
- Users can see the details of a delivery order.
- Admin can change the status and present location of a parcel delivery order.
 
## Click here to view the project demo pages
[SendIT](https://felixkiryowa.github.io/SendIT/)
When one visits that link they will be displayed with a site dashboard which welcomes them.
At the top they can choose to login if they have an account already or they can click on signup and register for an account.

But for now to login a user can type in 
    Click on the login button and you will be displayed with the users dashboard where the user can interact more with the system.

On top  there are navifgation menus which the user can use to perform their desired tasks on the website.

On the Administrator side 
They go to this link  https://felixkiryowa.github.io/SendIT/admin_dashboard.html
They are able to perform all their actions on the website using that dashboard.

## Built Using
- [HTML](https://html.com/) - Markup language


## Known Bugs
This website has no database so it may not store data sent to it.

## Authors
- [felixkiryowa](https://github.com/felixkiryowa/)

## Acknowlegments
 - [W3schools](https://www.w3schools.com/) Online Web Tutorials
 
## Contact me 
- Email:franciskiryowa68@gmail.com
- Phone Number:+256700162509
- Address:Lubaga


### Getting Started

Clone the project using the [link](https://github.com/felixkiryowa/SendIT.git).

### Prerequisites

A browser with the access to the internet.

### Installing

* Clone the project to your local machine
```
git clone https://github.com/felixkiryowa/SendIT.git
```

### Features

* Post a question
* Post an answer for a particular question
* Get all questions
* Get a single question
* Delete a question that a user has created
* A user can login
* A user can register
* A user can select a particular answer as the preferred one to the question he/she asked
* A user can edit an answer they have posted



### Endpoints

HTTP Method|Endpoint|Functionality
-----------|--------|-------------
POST|api/v1/questions|Create a question
GET|api/v1/questions/<questionId>|Fetch a specific question
GET|api/v1/questions|Fetch all questions
POST|api/v1/questions/<questionId>/answers|Add an answer
DELETE|api/v1/questions/<questionId>|Delete a question
POST|api/v1/auth/login|Allow a user to login
POST|api/v1/auth/signup|Allow a user to register and use the system
PUT|api/v1/questions/<questionId>/answers/<answerId>|Allow a user to mark an answer as preferred and edit an answer they provided


### Tools Used

* [Flask](http://flask.pocoo.org/) - Web microframework for Python.
* [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create isolated Python environments
* [PIP](https://pip.pypa.io/en/stable/) - Python package installer.


### Deployment

The API is hosted on [Heroku](https://kengo-stackoverflow-lite-api.herokuapp.com/api/v1/questions).

### Built With

* Python/Flask

### Authors

Kengo Wada