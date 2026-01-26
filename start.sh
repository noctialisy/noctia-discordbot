#!/usr/bin/env bash

git config --global --add safe.directory /usr/src/app
git pull
/usr/src/app/venv/bin/python main.py