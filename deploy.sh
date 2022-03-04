#!/bin/bash

# Assuming Ubuntu OS

# Install docker
sudo snap install docker
# Make docker run for non-sudo users
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo chmod 666 /var/run/docker.sock
newgrp docker

# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


# Docker volume for web/app/db
mkdir -p volumes/web
mkdir -p volumes/app
mkdir -p volumes/db

# Docker volume for logs
mkdir -p volumes/web/logs
mkdir -p volumes/app/logs

# Docker volume for postgres data
mkdir -p volumes/db/pgdata 

# Docker volume for managing certs
mdkir -p volumes/web/certbot/www/
mkdir -p volumes/web/certbot/certificates