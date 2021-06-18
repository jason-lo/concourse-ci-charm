#!/bin/sh

#
# This file is managed by Juju.  Attempt no changes here.
#

# Download concourse-ci
echo "Downloading Concours CI ..."

curl -O https://concourse-ci.org/docker-compose.yml
docker-compose up -d
