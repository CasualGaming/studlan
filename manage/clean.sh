#!/bin/bash

# venv
rm -rf .venv

# studlan
rm -rf /tmp/studlan
rm -rf static
rm -rf tmp
rm -rf log
rm -f studlan/settings/local.py

# Python
pyclean .
find . -name "*.pyc" -exec rm -rf {} \;
rm -rf *.egg-info
