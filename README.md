# Github API scraper service

## Description

Simple Github Repo and User data scraping service

### RESTful endpoint structure

| Endpoint | HTTP Method | CRUD Method | Result |
| --- | --- | --- | --- |
| users | GET | READ | Get all users
| users/:id|GET|READ| Get a single user
| users/:id/repos|GET|READ|Get all repos of a user
| users/|POST|CREATE| Add a single user
| users/:id|PUT|UPDATE| Update a single user
| users/:id|DELETE|DELETE|Delete a single user
| repos | GET | READ | Get all repos
| repos/:id|GET|READ| Get a single repo
| repos/:id/owner|GET|READ|Get owner of repo
| repos/|POST|CREATE| Add a single repo
| repos/:id|PUT|UPDATE| Update a single repo
| repos/:id|DELETE|DELETE|Delete a single repo
| next_url/repo|GET|READ|Get next link for repos
| next_url/repo|POST|CREATE|Create next link for repos
| next_url/repo|PUT|UPDATE|Update next link for repos
| next_url/repo|DELETE|DELETE|Delete next link for repos
| next_url/user|GET|READ|Get next link for users
| next_url/user|POST|CREATE|Create next link for users
| next_url/user|PUT|UPDATE|Update next link for users
| next_url/user|DELETE|DELETE|Delete next link for users



## Requirements

## Install

## Usage


