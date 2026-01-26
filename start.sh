#!/usr/bin/env bash

cd /usr/src/app
git config --global --add safe.directory /usr/src/app
git pull
/usr/src/app/venv/bin/python main.py