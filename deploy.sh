#!/bin/bash

# For Ubuntu OS

echo "Untar deploy folder"
tar -xvf deploy_artifacts.tar.gz

echo "Install docker"
# Install docker
sudo snap install docker
# Make docker run for non-sudo users
sudo groupadd docker
sudo gpasswd -a $USER docker
sudo touch /var/run/docker.sock
sudo chmod 666 /var/run/docker.sock


echo "Install docker-compose"
# Install docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose


echo "Install certbot"
sudo snap install --classic certbot 

echo "Create dirs"
# Create folders
cd ~
mkdir -p apihome/docker

cd ~/apihome/docker

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
mkdir -p volumes/web/nginx/conf
mkdir -p volumes/web/certbot/www/
mkdir -p volumes/web/certbot/certificates


# Pull images
echo "Docker login"
cd ~/apihome/docker
cp ~/deploy_artifacts/docker_login_password.txt .
cat docker_login_password.txt | sudo docker login --username sgshanks --password-stdin

echo "Pulling docker images"
sudo docker pull sgshanks/apihome:ui
sudo docker pull sgshanks/apihome:backend
sudo docker pull sgshanks/apihome:db

echo "Copy start and stop scripts to docker dir"
cp ~/deploy_artifacts/start.sh ~/apihome/docker
cp ~/deploy_artifacts/stop.sh ~/apihome/docker

echo "Copy docker compose script"
cp ~/deploy_artifacts/docker-compose.yaml ~/apihome/docker

echo "Copy nginx conf"
cp ~/deploy_artifacts/apihome_on_prem_80.nginx ~/apihome/docker/volumes/web/nginx/conf/apihome_on_prem_80.nginx

echo "Make docker non-sudo"
newgrp docker

exit