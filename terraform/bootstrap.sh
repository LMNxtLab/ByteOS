#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y docker.io docker-compose python3-pip
pip3 install flask requests openai

# Install Terraform
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform

# Enable and start Docker
sudo systemctl enable docker
sudo systemctl start docker
