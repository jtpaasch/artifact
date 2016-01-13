#!/bin/bash

# Print out what we're doing, and exit on first error.
set -x -e

# Install docker.
yum install -y docker

# Start the docker service.
service docker start
chkconfig docker on

# Pull down the docker image.
docker pull jtpaasch/simplepythonserver

# Now run the container.
docker run \
       --name my_app \
       --restart always \
       -d \
       -t \
       -i \
       -p 80:80 \
       jtpaasch/simplepythonserver:latest
