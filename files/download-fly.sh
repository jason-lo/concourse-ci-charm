#!/usr/bin/env bash

concourse_fqdn=$(hostname -i)

curl --noproxy ${concourse_fqdn} -s -f -o /root/fly "http://${concourse_fqdn}:8080/api/v1/cli?arch=amd64&platform=linux"
chmod u+x /root/fly

/root/fly --target=demo login \
    --concourse-url="http://${concourse_fqdn}:8080" \
    --username=test \
    --password=test \
    --team-name=main

mv /root/fly /usr/local/bin/
