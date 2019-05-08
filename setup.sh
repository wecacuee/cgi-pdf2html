#!/bin/bash
command -v docker || {
    echo "Install docker " && sudo apt-get install docker
}
command -v docker-compose || {
    echo "Install docker-compose" \
    && sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
}
nohup docker-compose up

