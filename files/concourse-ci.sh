#!/bin/sh

#
# This file is managed by Juju.  Attempt no changes here.
#

# Download concourse-ci
echo "Downloading Concours CI ..."

echo $1
if [ -z $1 ] || [ "$1" = "start" ];then
    rm -f /root/docker-compose.yml
    curl -o /root/docker-compose.yml -O https://concourse-ci.org/docker-compose.yml
    export hostip=$(hostname -i)
    sed -i 's/localhost/${hostip}/g' /root/docker-compose.yml
    docker-compose -p concourse-ci -f /root/docker-compose.yml up -d
elif [ "$1" = "stop" ];then
    export hostip=$(hostname -i)
    docker-compose -p concourse-ci down
elif [ "$1" = "restart" ];then
    docker-compose -p concourse-ci down
    sleep 20
    rm -f /root/docker-compose.yml
    curl -o /root/docker-compose.yml -O https://concourse-ci.org/docker-compose.yml
    export hostip=$(hostname -i)
    sed -i 's/localhost/${hostip}/g' /root/docker-compose.yml
else
    echo "You have gave the wrong value $1, it should be (start|stop|restart)."
fi
