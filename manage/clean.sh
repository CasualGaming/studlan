#!/bin/bash

# venv
rm -rf .venv

# tmpdir
rm -rf tmp

# Django
rm -rf static
rm -f studlan/settings/local.py

# Python
pyclean .
find . -name "*.pyc" -exec rm -rf {} \;
rm -rf *.egg-info
