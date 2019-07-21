#!/bin/bash

# Remove local run data, virtualenv, Python caches, etc.

echo "Cleaning virtualenv ..."
rm -rf .venv

echo "Cleaning Python cache ..."
find . -name "*.pyc" -exec rm -rf {} \;

echo "Cleaning local data ..."
rm -rf .local
rm -rf VERSION

echo "Cleaning config ..."
rm -f studlan/settings/local.py
rm -f studlan/settings/local.docker.py

echo "Cleaning Docker ..."
docker-compose -f setup/docker-compose.dev.yml down
docker-compose -f setup/docker-compose.test.yml down
