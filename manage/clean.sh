#!/bin/bash

pyclean .
find . -name "*.pyc" -exec rm -rf {} \;
rm -rf *.egg-info
