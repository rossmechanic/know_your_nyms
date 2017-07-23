# Know Your Nyms

## Project Setup (Requires database access)

First, run

**pip install -r requirements.txt**

from the project root directory.


### Gain access to the AWS console.

Go to *RDS/DB Instances/know-your-nyms-dev*, and use instance actions to see details.
Click on the security group, and visit that group's inbound traffic list. 
Add a source to the list, using *TCP*, *your IP* and *port 5432 (PostgreSQL)*.

You now can access the dev server database from your local copy! 


### Running locally

Use the command

**python manage.py runserver**

to run it locally. However, this still uses the development server database. 
It may be slow as a result, but it's not indicative of slow code.


## Deploying

First, obtain access keys for the server, and install awscli and ebcli. 

### awscli

Use the command

**aws configure**

to set up awscli along with the access keys you obtained and set the region to us-west-2.

### ebcli

Use the command

**eb init -i**

to set up elastic beanstalk for deploying, with these answers:

**Region:** us-west-2

**Application:** know-your-nyms

**Environment:** know-your-nyms-dev

**Using Python:** Yes

**Python Version:** 2.7

**Code Commit:** No

**SSH**: Yes

### Deploy

Use the command

**eb deploy**

to actually deploy to the server.

### Various

Use the command

**eb open** 

to view the dev server application.


Use the command 

**eb console** 

to open the console.



