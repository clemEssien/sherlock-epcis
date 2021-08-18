#!/bin/bash
#
# sudo apt-get install python-venv
#
echo "Setting up Python environment for Linux..."

python3 -m venv ./env
source env/bin/activate
pip3 install -r requirements.txt
bash mkworkdir.sh
echo "Setup Complete."
