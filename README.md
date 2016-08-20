# uServices
Storage for a container based microservices experiment using Docker Toolbox and PowerShell.

## Overview
This was an experimental project with the goal of developing a set of microservices as a learning experiment. It needed to take some input, do a few stages of processing and then post the results into ElasticSearch where some analytics could be done in Kibana.

The chosen problem was to feed 'books' into the service, which would then split it down successively, adding more data in the process, and eventually storing the page number and more specific location of each instance of each word in the book, so that things like frequency could be looked at.

The primary purpose was a learning objective, around the concept of microservices and using docker. A secondary objective was to try to get it working with a little implementation as possible.

The services are implemented as Python or Python/FlaskRESTful applications in Docker cotainers.

## Services
There are several services involved:
* RabbitMQ - Manages the message queues.
* ReadWorker - Has a POST endpoint where text data can be posted (see Data/testdata.json). It pushes the input to RabbitMQ.
* Divider - It takes the text from RabbitMQ, divides it into pages, and pushes the pages back to a different queue.
* Processor - Takes the pages from RabbitMQ and further processes them to push data specifically about each word to RabbitMQ.
* WriteWorker - Pulls the word message from RabbitMQ and indexes them in ElasticSearch.
* ElasticSearch - Stores and allows for querying of the processed information.
* Kibana - Visualises ElasticSearch.

## How to use it
To run this as is, you'll need to have Docker installed, and PowerShell.
There are 2 main scripts to run from PowerShell:

```
.\Scripts\Run.ps1
```
This will start a Docker machine, build the containers and run everything with some default parameters. Explore the file to see what can be passed in.

Once you've done this, try POSTing the contents of testdata.json to:
```
http://<machineip>:80
```
The RunAll script prints the machine ip as one of the last things it does to make this easily accessible. You can monitor the message queue here:

```
http://<machineip>:15672

user: guest
pass: guest
```
Finally, when you want to look in Kibana, navigate to:

```
http://<machineip>:5601
```
It will prompt you to create an index, untick "Index contains time-based events" and enter "words" as the index name and create the index.
When you've finished, you can use this script:

```
.\Scripts\StopAll.ps1
```
This will safely stop and remove all containers, then stop and remove all Docker machines.

## Additional
There is a template container for a flaskRESTful service in:

```
.\Containers\Flask_Template
```
This is a tested minimal container with a flaskRESTful service and a simple GET endpoint. It's provided as a starting point for creating your own.
