# Task List MCP Server
## Overview

This is a simple MCP Server demonstration. It deploys a Task List server onto google infrastructure. There is not external state for the application. It stores task list state inside a local json file that is updated and returned from MCP tool queries.

See the [documentation](documentation/) directory for more information


## Development
### Local Development

```bash
cd TaskListMCPServer/
uv virtualenv
source .venv/bin/activate
uv sync
uv run --env-file dev.env -- fastmcp run main.py --host 0.0.0.0 --transport streamable-http --port 8080
```

## Deployment
We will be deploying with Google. Our deployment solution will be a simple Virtual Machine (VM) instance.

In order to do that we need to perform some initial steps

```bash
# ------------------------------------------------------------------------------
# Set initial environment variables for our commands
# ------------------------------------------------------------------------------
PROJECT_ID="FILL_IN"
SERVICE_ACCOUNT_ID="FILL_IN"
SERVICE_ACCOUNT_DISPLAY_NAME="Service Account for Task List MCP Server VM"
SERVICE_ACCOUNT_EMAIL="${SERVICE_ACCOUNT_ID}@${PROJECT_ID}.iam.gserviceaccount.com"

IMAGE_REGISTRY_URL="FILL_IN"
IMAGE_REGISTRY_PROJECT="FILL_IN"
IMAGE_REGISTRY_REPOSITORY="FILL_IN"
IMAGE_TAG="task-list-mcp-server"
IMAGE_VERSION="0.0.0"
IMAGE_FULL_URL=${IMAGE_REGISTRY_URL}/${IMAGE_REGISTRY_PROJECT}/${IMAGE_REGISTRY_REPOSITORY}/${IMAGE_TAG}:${IMAGE_VERSION}

VM_NAME="task-list-mcp-server"
VM_ZONE="us-west1-a"
VM_MACHINE_TYPE="e2-medium"
VM_IMAGE_FAMILY="debian-11"
VM_IMAGE_PROJECT="debian-cloud"
VM_BOOT_DISK_SIZE="20GB"
VM_METADATA_FROM_FILE="startup-script=./google_cloud_platform/gcloud_startup_script.sh"
VM_TAGS="http-server"
VM_SERVICE_ACCOUNT="${SERVICE_ACCOUNT_EMAIL}"
VM_SCOPES="cloud-platform"
```

```bash
gcloud auth configure-docker ${IMAGE_REGISTRY_URL}
gcloud auth print-access-token | podman login -u oauth2accesstoken --password-stdin ${IMAGE_REGISTRY_URL}

gcloud config set project "${PROJECT_ID}"
```

### Build Docker Image
```bash
# Build Docker Image
podman build --platform linux/amd64 \
             --file ./docker/task_list_mcp_server.Dockerfile \
             --tag ${IMAGE_FULL_URL} \
             .

# Run Locally
podman run -p 8080:8080 \
           --env-file ./docker/local.env \
           -it ${IMAGE_FULL_URL}
```

### Publish Docker Image
```bash
podman push ${IMAGE_FULL_URL}
```

### Deploy Docker Image
```bash
# ------------------------------------------------------------------------------
# Create a service account (Perform Once)
# ------------------------------------------------------------------------------
gcloud iam service-accounts create "${SERVICE_ACCOUNT_ID}" \
        --display-name="${SERVICE_ACCOUNT_DISPLAY_NAME}" \
        --project="${PROJECT_ID}"

# ------------------------------------------------------------------------------
# Grant required permission (Perform Once)
# - Read objects in Google Cloud Storage
# - Read artifacts in Artifact Registry
# ------------------------------------------------------------------------------
gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/storage.objectViewer"

gcloud projects add-iam-policy-binding "${PROJECT_ID}" \
    --member="serviceAccount:${SERVICE_ACCOUNT_EMAIL}" \
    --role="roles/artifactregistry.reader"

# ------------------------------------------------------------------------------
# Create firewall rull to allow access to the VM (Perform Once)
# ------------------------------------------------------------------------------
gcloud compute firewall-rules create allow-http-80-all \
        --description="Allow HTTP traffic on port 80 to http-server tagged instances from anywhere" \
        --direction=INGRESS \
        --priority=1000 \
        --network=default \
        --action=ALLOW \
        --rules=tcp:80 \
        --source-ranges=0.0.0.0/0 \
        --target-tags=http-server

# ------------------------------------------------------------------------------
# Create the VM Instance
# ------------------------------------------------------------------------------
# This is the MacOS `sed` command. The '' should be removed for Linux machines
sed -i '' 's|REPLACE_IMAGE_FULL_URL|'"${IMAGE_FULL_URL}"'|g' ./google_cloud_platform/gcloud_startup_script.sh

gcloud compute instances create ${VM_NAME} \
        --zone ${VM_ZONE} \
        --machine-type ${VM_MACHINE_TYPE} \
        --image-family ${VM_IMAGE_FAMILY} \
        --image-project ${VM_IMAGE_PROJECT} \
        --boot-disk-size ${VM_BOOT_DISK_SIZE} \
        --metadata-from-file ${VM_METADATA_FROM_FILE} \
        --tags ${VM_TAGS} \
        --service-account="${SERVICE_ACCOUNT_EMAIL}" \
        --scopes ${VM_SCOPES}
```
