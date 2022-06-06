# Probending arena reservation
(big data and distributed system project)

## How to run
In `docker` directory:

to init cassandra cluster: `./setup.sh`

to stop the cluster `./stop.sh`

to start the cluster `./start.sh`

to eradicate all existing parts of cassandra `./cleanup.sh`

`chmod +x [script name]` may be required

run `main.py`

## Motivation
In our project, we decided to create a distributed reservation system for our favorite cartoon-based game - Probending competition. For those interested, rules can be found [here](https://avatar.fandom.com/wiki/Pro-bending). Although in the original series there are only two arenas mentioned, we decided to use our exquisite imagination to define a few additional. After all it is a big data project, right?

## Technology
We decided to use the supreme programming language called Python3. In addition, we utilize a distributed database system - Cassandra. Everything is connected by our lord and savior - docker container.

## Executive summary
We implemented several services that together create the core of our application. Each service has its own functionality. We can distinguish the most important services:
- CassandraConnector - a service responsible for connecting to the database, it can be considered as a client of the system.
- ReservationSystem - the very core of our application - implements the logic underlying the reservations.
- QueryEngine - a class implementing facade methods for generating query - it’s goal is to hide the pure queries from the user
- Tester - a utility class that implements three stress tests, which emphasize Cassandra's pros and cons. 
- db - a simple framework for initialization of the database

In addition, we run our database in the distributed manner, on 3 separate nodes. In case one node fails, the system is still able to work flawlessly.
The schema of the system can be found in the file `DB-schema.pdf`.

## Problems
At first, we tried to work on 4 Cassandra nodes, however with the RAM we had on our computers, it was not possible to run them. We quickly fixed this problem, by restraining the number of nodes to 3 and limiting RAM usage for the containers, for presentation purposes. 

The main issue to overcome for us was the transition from relational databases to Cassandra. At first, we designed a schema, which was heavily based on the SQL databases and we had problems with queries, since in Cassandra, one can filter only by keys. 

After getting the understanding of how things work in Cassandra, we redesigned databases, used lists for storing the seats instead of a separate table to have easy access to available seats for each game. With this approach, we were able to create a well-working system.
