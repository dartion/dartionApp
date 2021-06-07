#!/bin/sh
# Initialise Cockroach Database
#docker-compose exec baseApp-db /cockroach/cockroach init --insecure
docker exec dartionApp-db /cockroach/cockroach sql --insecure --execute="CREATE USER 'dartion_app_db_user';"
docker exec dartionApp-db /cockroach/cockroach sql --insecure --execute="CREATE DATABASE IF NOT EXISTS dartion_app_db;"
docker exec dartionApp-db /cockroach/cockroach sql --insecure --execute="GRANT ALL ON DATABASE dartion_app_db TO dartion_app_db_user;"
