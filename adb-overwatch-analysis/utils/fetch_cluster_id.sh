#!/bin/bash

# Replace with your Databricks instance URL and token
DATABRICKS_HOST="https://<your-databricks-instance>"
DATABRICKS_TOKEN="<your-databricks-token>"
CLUSTER_NAME="My Existing Cluster"

# Fetch the cluster ID by name
CLUSTER_ID=$(databricks clusters list --output JSON | jq -r --arg name "$CLUSTER_NAME" '.clusters[] | select(.cluster_name == $name) | .cluster_id')

# Export the cluster ID as an environment variable
export TF_VAR_existing_cluster_id=$CLUSTER_ID