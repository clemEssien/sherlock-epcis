#!/bin/bash

echo "Creating working directories..."

sudo mkdir /usr/src
sudo mkdir /usr/src/documents
sudo mkdir /usr/src/uploads

ml=$USER
sudo chown $ml.$ml /usr/src -R


