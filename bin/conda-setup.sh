#!/bin/bash
# This script sets up the Conda environment for the project.
#
APP_PATH=$(dirname "$0")
enviro=$(basename "$PWD")

# Check if the environment exists
if ! conda env list | grep -q "$enviro"; then
    echo "Creating a new conda environment named $enviro..."
    # Create a new conda environment named "$enviro" using the configuration file "conda_config.yaml"
    conda create --name $enviro --file ../conf/c-requirements.txt -y
fi

echo " ------------------------------ "
echo "conda activate "$enviro
echo " ------------------------------ "
echo "pip install -r conf/p-requirements.txt"
echo " ------------------------------ "
