#!/bin/bash

# Print out what we're doing, and exit on first error.
set -x -e

# Install docker.
yum install -y docker

# Start the docker service.
service docker start
chkconfig docker on

# Authenticate with docker.
docker login \
       -u 'mechanicalautomaton' \
       -p 'Dp#6B7quM6nepMXvp4qdJv%V' \
       -e 'mechanical.automaton@gmail.com'

# Pull down the private docker image.
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
