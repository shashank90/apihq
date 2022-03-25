#! /bin/bash


# from ~/apihome/docker
docker-compose -f docker-compose-cert-renew.yaml run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d www.test.apihome.io