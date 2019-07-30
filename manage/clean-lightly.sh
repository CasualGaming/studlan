#!/bin/bash

# Remove some local data and Python cache files

echo "Cleaning Python cache ..."
find . -name "*.pyc" -exec rm -rf {} \;

echo "Cleaning some local data ..."
rm -rf .local/venv/log
rm -rf .local/docker/log
