#!/bin/bash

# Python
pyclean .
find . -name "*.pyc" -exec rm -rf {} \;
rm -rf *.egg-info

# venv
rm -rf .venv

# tox
rm -rf .tox
