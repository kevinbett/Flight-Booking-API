[![Build Status](https://travis-ci.com/kevinbett/Flight-Booking-API.svg?branch=ft-add-passport-167105135)](https://travis-ci.com/kevinbett/Flight-Booking-API)
[![Maintainability](https://api.codeclimate.com/v1/badges/4c656883a42b03c6e3d1/maintainability)](https://codeclimate.com/github/kevinbett/Flight-Booking-API/maintainability)
# Flight Booking API

The flight booking application enables users to book flights, upload their passport images and get reminders when their flights are due.

# Key Features

Users are able to perform the following functions;

> * Sign up for an account
> * Log in into the application
> * Upload a passport images
> * Edit a passport images
> * Delete a passport image
> * Add a flight
> * Book a flight
> * Get flight reminders

# Prerequisites

Have Python installed

# Built With

* Python Flask
* SQLAlchemy

# Api Installation

To set up the Flight Booking API, make sure that you have Python, postman and pip installed.
Use virtualenv for modules management.
## Running the API
**EndPoint** | **Functionality**
--- | ---
POST `/auth/register` | Register user account
POST `/auth/login` | login user
POST `/passport/image` | upload passport
DELETE `/passport/image` | delete passport
POST  `/flight/createflight` | Create a flight
POST `/booking/flightbooking` | Book a flight
GET  `/flight/getbookings` | Gets all bookings per flight

# Contributing

1. Fork this project to your GitHub account.
2. Create a branch for version control.
3. Proceed to make modifications to your fork.
4. Send pull request from your fork's branch to my master branch.

# Guidelines | How to run the app and tests

- create a virtual environment and install flask.
- Run `python manage.py runserver` to execute the server
- To test the application, run `python manage.py test`.

# Author

* Kevin Bett
