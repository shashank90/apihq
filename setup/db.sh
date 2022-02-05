#!/bin/bash

# sudo apt update

# sudo apt install postgresql postgresql-contrib


# Follow instructions to add user: 
# https://stackoverflow.com/questions/27107557/what-is-the-default-password-for-postgres
# TODO: Automate these steps 
# 1. Make `postgres` authentication to `trust` in file /etc/postgresql/12/main/pg_hba.conf
# 2. Change `postgres` user password (alter user postgres password <newpassword>;)
# 3. Reset trust to md5 for postgres and other users in pg_hba.conf file 
# 4. sudo service postgresql restart

# Create user with password and role
psql -U postgres -c "CREATE USER p075am WITH PASSWORD 'Wyr73x@BgQQ;4' CREATEDB;"
