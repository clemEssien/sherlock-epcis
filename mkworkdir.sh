#!/bin/bash

echo "Creating working directories..."

sudo mkdir /var/src
sudo mkdir /var/src/documents
sudo mkdir /var/src/uploads

thisos=$(uname)
ml=$USER

if [[ $thisos -eq "Darwin" ]]; then
    sudo chown -R $ml /var/src
else
    sudo chown $ml.$ml /var/src -R
fi





