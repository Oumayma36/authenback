REM Build the new authenticate container
docker-compose build authenticate

REM Run the new authenticate container
docker-compose up -d authenticate