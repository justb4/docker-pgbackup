#!/bin/bash

# Stop and remove possibly old containers
docker-compose stop
docker-compose rm -f

# Finally run
docker-compose up -d


