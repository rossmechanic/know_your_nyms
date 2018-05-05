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

Follow the instruction here to get access to the AWS database

https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html

### Installing database locally

```
brew install postgres
initdb -D ~/know-your-nyms/
pg_ctl start -D ~/know-your-nyms/
createdb know-your-nyms

createuser --superuser --createdb --createrole --login --pwprompt --encrypted know-your-nyms

# Documentation for createuser command (wrapper around psql #= CREATE USER ... )
# http://www.postgresql.org/docs/8.3/static/app-createuser.html
```

Quick-reference for useful Postgres commands:

```
# Start server:
pg_ctl start -D ~/know-your-nyms

# Stop server:
pg_ctl stop -D ~/know-your-nyms

# Start server on system start-up (make sure the plist settings match the settings above):
ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
```

### Running locally

Use the command

```
python manage.py runserver
```

to run it locally. However, this still uses the development server database. 
It may be slow as a result, but it's not indicative of slow code.

If you made a changes to models.py, run

```
python manage.py makemigrations
python manage.py migrate
```
before running

```
python manage.py runserver
```

To test, run
```
python manage.py test
```

To pre-populate a database locally, run
```
python manage.py loaddata data.json
```
where data.json is your json file that you want to upload
For more information see django docs on fixtures
code for making such fixtures is under 
```
makefixtures.py
```

Decompress original_pictures_vocab.txt.zip locally to run the pictures game