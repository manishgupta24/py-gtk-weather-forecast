#!/bin/bash

# Exit on error
set -e

echo "Installing dependencies"
apt install -y python3-dev python3-pip python3-venv libcairo2-dev python3-gi python3-gi-cairo gir1.2-gtk-3.0 libgirepository1.0-dev

echo "Creating python virtual environment"
python3 -m venv env

echo "Installing pip packages"
env/bin/pip install -r requirements.txt
