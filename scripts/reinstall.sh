#!/bin/bash
set -e

pip uninstall -r ../requirements.txt -y
pip install -r ../requirements.txt
echo -e "\nSuccessfully reinstalled packages."
