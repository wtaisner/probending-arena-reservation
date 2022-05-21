#./cleanup.sh

docker run --name cass1 -p 9042:9042 -e CASSANDRA_CLUSTER_NAME=ProbendingCluster -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -d cassandra:latest
docker run --name cass2 -e CASSANDRA_SEEDS="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' cass1)" -e CASSANDRA_CLUSTER_NAME=ProbendingCluster -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -d cassandra:latest
docker run --name cass3 -e CASSANDRA_SEEDS="$(docker inspect --format='{{.NetworkSettings.IPAddress}}' cass1)" -e CASSANDRA_CLUSTER_NAME=ProbendingCluster -e HEAP_NEWSIZE=1M -e MAX_HEAP_SIZE=1024M -d cassandra:latest

docker inspect --format='{{.NetworkSettings.IPAddress}}' cass1
docker inspect --format='{{.NetworkSettings.IPAddress}}' cass2
docker inspect --format='{{.NetworkSettings.IPAddress}}' cass3
