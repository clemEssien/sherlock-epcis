#!/bin/bash
#
# sudo apt-get install python-venv
#
python3 -m venv ./env
source env/bin/activate
pip3 install -r requirements.txt
