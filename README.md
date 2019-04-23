# Fullstack Fundamentals

## What is it?
This is my repository containing my exercise code from Udacity's Full Stack Foundations course (https://www.udacity.com/course/full-stack-foundations--ud088). My solution code differs from Udacity's solutions code (https://github.com/udacity/Full-Stack-Foundations/) due to me using Python 3.6.7 instead of Python 2x.

## Status
_Complete._ Only maintenance updates now.

## How do I use it?
Each module is divided into its own folder. To initially set up a module, do the following:

* `cd` into a module folder;
* Create a Python 3.6.7 virtual environment: `virtualenv env`;
* Activate the Python virtual environment: `source env/bin/activate`;
* Install dependencies: `pip install -r requirements.txt`;
* Create the SQLite DB by running the Python scripts database_setup.py and lotsofmenus.py in that order.

Once you have performed the above, you can then simply run the relevant script (usually webserver.py or crud-webserver.py) to start the server up on port 8080. Control+C terminates the webserver and executing `deactivate` deactivates the Python virtual environment.
