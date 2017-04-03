# Simple blog


This is an illustration of a simple blog app that provides a few functionalities. 

* You can see individual posts
* You can see all posts
* You can search for posts
* You can create and edit posts 

## Installing

Install the requirements for the app. 

    pip install -r requirements.txt

You then need to export an environment variable to be able to run the app itself. 

    export FLASK_APP=app.py 

The app uses sqlite as a database and we want to populate the database with some entries. You can do this with the following command

    flask initdb

Now it's time to kickstart the app and see what it looks like!

    flask run

As you can see in the command interface the app is running on `localhost:5000`

To make sure that all tests are passing you can run the following command

    flask tests
