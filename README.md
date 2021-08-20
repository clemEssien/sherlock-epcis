[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Version badge](https://img.shields.io/badge/version-0.0-purple.svg)](https://shields.io/)

# README 

This README documents the steps necessary to get your application up and running.

### What is this repository for?

#### Quick summary 
sherlock-epcis is the backend server responsible for converting EPCIS GS1 data to FDA CTEs & KDEs for reporting purposes.

## Content

* [FlaskAPI](#FlaskAPI)
* [Database Configuration](#Database-configuration)
* [EPCIS Event Classes](#EPCIS-Event-Classes)
* [CTE Classes](#CTE-Classes)
* [Contribution guidelines](#Contribution-guidelines)


## FlaskAPI

## Database configuration
Sherlock-epcis uses Neo4j 4.1.9
The following modifications need to be made to the configuration file
- sudo nano /etc/neo4j/neo4j.conf (elevated privileges are required for this operation) 
- Uncomment line 70 i.e. dbms.default_listen_address=0.0.0.0  
- Uncomment lines 94-96 

```dbms.connector.http.enabled=true 
dbms.connector.http.listen_address=:7474 
dbms.connector.http.advertised_address=:7474
```

### EPCIS Event Classes

### CTE Classes

### Contribution guidelines ###

#### Writing tests ####
We use [pytest](https://github.com/pytest-dev/pytest) for unit tests.

#### Code review and PRs ####
* Always assign your hierarchal buddy as your reviewer in addition to the defaults. 
* Please also include changes to the ReadMe in your PRs as needed.
* Please name branches using the following schema `<prefix>/<JIRA-ticket-ID>-description` where:
	* prefix is either `feature`, `hotfix`, `release` or `bugfix` depending on the type of task.
	* Jira ticket ID is the ticket number for the given feature in JIRA example `TNT-1`.

Please follow the following guides to PRs:

* [A guide to effective PR reviews](https://nebulab.com/blog/a-guide-to-effective-pull-request-reviews)
* [Good vs. Bad PR requests](http://allyouneedisbackend.com/blog/2017/08/24/pull-requests-good-bad-and-ugly/)

#### Other guidelines ####

### Who do I talk to? ###

#### Repo owner or admin ####
Nathaniel Moschkin (nathaniel.moschkin@precise-soft.com)

#### Other community or team contact ####
Abdullah Yusuf (abdullah.yusuf@precise-soft.com)

[Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)