#!/bin/bash

cd "$(dirname "$(realpath "$0")")"

source ./venv/bin/activate
python3 main.py
exit
