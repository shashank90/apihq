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