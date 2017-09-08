# Know Your Nyms

## Project Setup (Requires database access)

First, run

```
pip install -r requirements.txt
```

from the project root directory.


### Gain access to the AWS console.

Go to *RDS/DB Instances/know-your-nyms-dev*, and use instance actions to see details.
Click on the security group, and visit that group's inbound traffic list. 
Add a source to the list, using *TCP*, *your IP* and *port 5432 (PostgreSQL)*.

You now can access the dev server database from your local copy! 


### Running locally

Use the command

```
python manage.py runserver
```

to run it locally. However, this still uses the development server database. 
It may be slow as a result, but it's not indicative of slow code.

