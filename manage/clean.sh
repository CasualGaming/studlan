#!/bin/bash

# Remove local run data, virtualenv, Python caches, etc.

echo "Cleaning virtualenv ..."
rm -rf .venv

echo "Cleaning Python cache ..."
find . -name "*.pyc" -exec rm -rf {} \;

echo "Cleaning local data ..."
rm -rf .local

echo "Cleaning config ..."
rm -f studlan/settings/local.py
