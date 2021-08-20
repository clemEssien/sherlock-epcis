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
  - [Neo4j service setup](#Neo4j-service-setup)
  - [Graph algorithms](#Graph-algorithms)
  - [Json file import](#Json-file-import) 
* [EPCIS Event Classes](#EPCIS-Event-Classes)
* [CTE Classes](#CTE-Classes)
* [Contribution guidelines](#Contribution-guidelines)


## FlaskAPI

## Database configuration
Sherlock-epcis uses [Neo4j 4.1.9](https://neo4j.com/download-center/)
### Neo4j service setup
The following modifications need to be made to the configuration file to run the service on port 7474
- sudo nano /etc/neo4j/neo4j.conf (elevated privileges are required for this operation) 
- Uncomment line 70 as follows: 
```
	dbms.default_listen_address=0.0.0.0 
``` 
- Uncomment lines 94-96 as follows:

``` dbms.connector.http.enabled=true 
	dbms.connector.http.listen_address=:7474 
	dbms.connector.http.advertised_address=:7474
```
### Graph algorithms
To enable graph algorithms, modify the neo4j config file located at /etc/neo4j/neo4j.conf as follows:
```
dbms.security.procedures.unrestricted=apoc.*,algo.*,gds.* 
dbms.security.procedures.allowlist=gds.*,apoc.load* 
dbms.security.procedures.whitelist=gds.*,apoc.* 
```
Then download the Algorithms and Graph Data Science libraries: 

[apoc-4.1.0.9-core.jar](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/download/4.1.0.9/apoc-4.1.0.9-core.jar) 

[neo4j-graph-data-science-1.6.2.jar](
https://github.com/neo4j/graph-data-science/releases/download/1.6.2/neo4j-graph-data-science-1.6.2.jar)

place them in the Neo4j plugins directory (i.e. /var/lib/neo4j/plugins)
### Json file import
To enable json file import into the Neo4j database, add the following lines at the end of the neo4j.conf file
```
apoc.import.file.enabled=true 
apoc.import.file.use_neo4j_config=false 
```
### EPCIS Event Classes

### CTE Classes

## Contribution guidelines ##

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