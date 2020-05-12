# Training Tracker
This is a web application developed in Django. 

## Goal
The main goal is to help sharing training routines in training groups, as well as to facilitate their tracking by both group members and the trainer.

Using this application you will be able to:
- Create training routines with your description and a link to a youtube video.
- Track your workout, uploading the time you spend on each routine. 
- Have a wide overview of your workout through the control panel on the home page. 
- Track the training of your students.


## Setting up

### Pre-requisites
- Python 3.7 or later
- Pipenv

### Start and configure local env
    $ pipenv shell
    $ pipenv install
    
### Migrate models and create superuser

    $ pipenv run python manage.py migrate
    $ pipenv run python manage.py createsuperuser
    


## Using

### Running server

    $ pipenv run python manage.py runserver
   
