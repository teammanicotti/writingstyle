# Team Manicotti Senior Project
The moment you've all been waiting for...is here!

## Requirements
- Python 3.6
- MySQL 8.0.18
- The Python packages listed below:
  - gunicorn
  - falcon
  - pytest (development only)
  - pylint (development only)
  - sentry-sdk[falcon]==0.13.1
  - python-dotenv
  - SQLAlchemy

_or_
* Docker

## Code Coverage & Pipeline Status
[![coverage report](https://gitlab.com/seniorprojectntid/seniorproject/badges/develop/coverage.svg)](https://gitlab.com/seniorprojectntid/seniorproject/commits/develop)
[![pipeline status](https://gitlab.com/seniorprojectntid/seniorproject/badges/develop/pipeline.svg)](https://gitlab.com/seniorprojectntid/seniorproject/commits/develop)

## How to Run
### Creating Database
Creating the database for local development can be done by importing the SQL
files located in the `db_init` folder into your MySQL instance.  Setting up
a MySQL instance is out of scope for this README, but is set up automatically
if running via Docker. 

### Creating Environment Files
For any of the below methods, environment files need to be created to tell the
application where to access the database and other resources.  The following
environment files are needed:
* `.db_name`
* `.db_url` (if using docker, simply put the value `database` in this file)
* `.db_user`
* `.db_password`
* `.db_root_password` (if running in Docker)
* `.sentry_dsn` (optional, for logging errors in Sentry)

These files do not follow the `envfile` convention, they instead
follow the Docker secrets convention of only containing the value itself. So
instead of putting `KEY=VALUE`, simply put `VALUE`.


### Docker (from repository)
1. Open the file `docker-compose-local-image.yml`.  For the `image:` line, edit
this to point to the URL of the image you want from the 
[Container Repository](https://gitlab.com/seniorprojectntid/seniorproject/container_registry).
The value after the colon can be a commit UUID, a tag name, or a branch name.
1. Login to the repository via Docker via 
`docker login registry.gitlab.com -u <gitlabUsername> -p <accessToken>`,
where `accessToken` is an API token created from 
[here](https://gitlab.com/profile/personal_access_tokens).
Only the `API access` permission is needed.
1. Run the command 
`docker-compose -f docker-compose.yml -f docker-compose-local-image.yml up`
in the project root directory, or use 
`docker-compose --build -f docker-compose.yml -f docker-compose-local-image.yml up -d`
to run it as a daemon.
### Docker (building image)
1. Run the command 
`docker-compose -f docker-compose.yml -f docker-compose-local.yml up`
in the project root directory, or use 
`docker-compose -f docker-compose.yml -f docker-compose-local.yml up -d`
to run it as a daemon.

* If running interactively, simply kill the application with `Ctrl+C`.
* To remove the container, run `docker-compose -f docker-compose.yml -f docker-compose-local.yml down`.
* If you've made changes and want to re-build, run the above commands with 
`--build` appended to force a re-build.
### Manual Setup
1. Run `pip install -r seniorproject/requirements.txt` from the root of the
project directory.
1. Then, run the application using the command `gunicorn seniorproject.api:API`.

* You can kill the application with `Ctrl+C`.
