# Github API scraper service

## Description

Simple Github Repo and User data scraping service that will batch fetch repos of users. It has endpoints for working with the stored data.

## Requirements

1. Python 3.8 or greater
1. Pipenv
1. Github personal token (optional)
1. Postman or similar API exploration tool

## Install

1. Clone this repo: `git clone git@github.com:asfourco/github_scraper.git` or unpack the tarball/archive in a project directory
2. Navigate to the project directory `cd /path/to/github_scraper`
3. Initiate a python virtual environment: `pipenv shell`
4. Install dependencies: `pipenv install`
5. Initialize the database: `python manage.py migrate`
6. (Optional) one can make authenticated calls against the Github API, which increases rate limits. To do so, add your *username* and *personal_access_token* in `/path/to/github_scraper/.env` as follows:  
```
USERNAME=_username_
ACCESS_TOKEN=_personal_access_token_
```
7. Start the service `python manage.py runserver`, and navigate to [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/) to start exploring the api. Alternatively, one can use a tool like [Postman](https://www.postman.com) to navigate and test the API endpoints

## Usage

A basic command would be:

```shell
# Fetch list of stored users
curl -L -X GET 'http://localhost:8000/api/v1/users'
```

This can be used with any of the endpoints listed below.

### Automated scraping endpoints

The service is capable of batch fetching users and their corresponding repos, and keep track of the link to the next page of data. This is useful when automating scraping with cron-jobs, for example:

```shell
# run this job at 0 minute of every 2nd hour, every day; throw away the output
0 */2 * * * curl -L -X GET 'http://localhost:8000/api/v1/scrape_github'  > /dev/null 2>&1
```

### Manual scraping endpoints

The service also can scrape repos of a specific user:

```shell
# let's assume we have a username of 'fizzybuzz'
curl -L -X GET 'http://localhost:8000/api/v1/scrape_user_repo/fizzybuzz'

# If we would like to just scrape the repos in which they are only the members, then
curl -L -X GET 'http://localhost:8000/api/v1/scrape_user_repo/fizzybuzz?type=member'
```

Apart from fetching returning the data, the service will also store the data.

## Endpoints

### RESTful endpoint structure
base url: `http://localhost:8000/api/v1`

| Endpoint | HTTP Method | CRUD Method | Result |
| --- | --- | --- | --- |
| /users | GET | READ | Get all users
| /users/:id|GET|READ| Get a single user
| /users/:id/repos|GET|READ|Get all repos of a user
| /users/|POST|CREATE| Add a single user
| /users/:id|PUT|UPDATE| Update a single user
| /users/:id|DELETE|DELETE|Delete a single user
| /repos | GET | READ | Get all repos
| /repos/:id|GET|READ| Get a single repo
| /repos/:id/owner|GET|READ|Get owner of repo
| /repos/|POST|CREATE| Add a single repo
| /repos/:id|PUT|UPDATE| Update a single repo
| /repos/:id|DELETE|DELETE|Delete a single repo

### Scraping Repos of a User Endpoint

#### Endpoint:

`/scrape_user_repo/:username`

#### Description

This endpoint will scrape the repos of a Github user. The following parameters can be used.

| Parameters | Type | In| Description|
|---|---|--|--|
|username|string|path||
|type|string|query|Can be one of **all**, **owner**, **member**.|
|sort|string|query|Can be one of **created**, **updated**, **pushed**, **full_name**.|
|direction|string|query|Can be one of **asc** or **desc**. Default: **asc** when using **full_name**, otherwise **desc**
|per_page|integer|query|Results per page (max 100)
|page|integer|query| Page number of the results to fetch.

### Automated scraping

#### Endpoint:
 
 `/scrape_github`

#### Description

The endpoint will continue scraping Github repos and users by first fetching the batch of users and scraping their respective repos. Note, Github API returns with pagination links. These are used to pickup where the last time the automated scrape run.

| Paramaters|Type|In|Description|
| -- | --| --|--|
|per_page|integer|query|Number of users per page (max 100, default 10)
|reset|bool|query|Ignore the next url pagination and start scraping from the beginning


## Contributing

Development tools we use are:
* `flake8` - code linting
* `bandit` - vulnerability scanner
* `black` - code formatter
* `pre-commit` - pre commit task runner, runs the other three tools prior to committing code to catch any issues *a priori*

To install `pre-commit` run the following in at the root of the project directory: `pre-commit install`. You can then use this tool independently of committing your changes: `pre-commit run -a` (runs all tools) or a specific tool: `pre-commit run flake8`.

### Testing

Unit tests for the service are located in `github_scraper/service/tests/`, while tests for the scraper code are located in `github_scraper/scraper/tests.py`. To run the tests:

```shell
# For all tests within the project
$ python manage.py test

# For all tests within an app in the project
$ python manage.py test service

# For a specific test
$ python manage.py test service.tests.test_model_user.GetSingleUserTest
```
