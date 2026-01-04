#!/bin/bash

# Stop and remove possibly old containers
docker compose down --remove-orphans

# Finally run
docker compose up -d


