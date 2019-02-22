#!/bin/bash

exec bash --init-file <(echo "source venv/bin/activate; trap deactivate EXIT") -i
