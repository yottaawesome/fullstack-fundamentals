# Fullstack Fundamentals

## What is it?
This is my repository containing my exercise code from Udacity's Full Stack Foundations course (https://www.udacity.com/course/full-stack-foundations--ud088). The code differs slightly from Udacity's code due to me using Python 3 with VirtualEnv. Additional modules will be added as I progress.

## How do I use it?
Each module is divided into its own folder. To initially set a module up, do the following:

* `cd` into a module;
* Create a Python 3 virtual environment: `virtualenv env`;
* Activate the virtual environment: `source env/bin/activate`;
* Install dependencies: `pip install -r requirements.txt`;
* Create the SQLite DB by running the Python scripts database_setup.py and lotsofmenus.py in that order;

Once you have performed the above, you can then simply run the webserver.py script to start the server up on port 8080.
