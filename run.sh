#!/bin/bash

# shut everything down from last time
docker compose down --remove-orphans

# start everything back up
docker-compose up -d --build
