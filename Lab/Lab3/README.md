# Lab 3 - Kafka

Kafka is a distributed streaming platform which can be used for building real-time data pipelines and streaming apps.

These are four main parts in a Kafka system:

* Broker: Handles all requests from clients (produce, consume, and metadata) and keeps data replicated within the cluster. There can be one or more brokers in a cluster.  
* Zookeeper: Keeps the state of the cluster (brokers, topics, users).  
* Producer: Sends records to a broker.  
* Consumer: Consumes batches of records from the broker.  



## Lab completion date - 02/05/2021

## Setup:

- Download Binaries: https://kafka.apache.org/downloads
- Setup Project in Pycharm with virtual environment
- Twitter developer account to generate API keys and bearer tokens


## Configuration:
```
$ pip3 install kafka-python
```

Once you unzip the binaries, navigate to the location on your local machine and run:
```
$ bin/zookeeper-server-start.sh config/zookeeper.properties
```
All the scripts are in Lab folder.

Trigger Kafka broker:
```
$ bin/kafka-server-start.sh config/server.properties
```
## CodeLab document:  
For more information on lab refer the [CodeLab Document](https://codelabs-preview.appspot.com/?file_id=1elvYBfSGrvoB3NuqWbCt4qWFycmci1cyspyYzYsJp7I#0)
