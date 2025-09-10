#!/bin/bash
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Set up the stable Docker repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list >/dev/null

# Install Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Configure docker to point to artifact registry
sudo gcloud auth configure-docker --quiet us-west1-docker.pkg.dev

# Run your Docker container in detached mode, mapping port 80 on the host to 8080 in the container
sudo docker run -d \
    --env TASK_LIST_JSON_FILE=task_list_database.json \
    -p 80:8080 \
    REPLACE_IMAGE_FULL_URL
