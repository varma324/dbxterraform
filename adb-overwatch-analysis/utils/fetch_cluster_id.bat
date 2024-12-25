@echo off
setlocal

:: Replace with your Databricks instance URL and token
set DATABRICKS_HOST="https://<your-databricks-instance>"
set DATABRICKS_TOKEN="<your-databricks-token>"
set CLUSTER_NAME=Shared_Autoscaling

:: Fetch the cluster ID by name
for /f "tokens=*" %%i in ('databricks clusters list --output JSON ^| jq -r --arg name "%CLUSTER_NAME%" ".clusters[] | select(.cluster_name == $name) | .cluster_id"') do set CLUSTER_ID=%%i

:: Export the cluster ID as an environment variable
set TF_VAR_existing_cluster_id=%CLUSTER_ID%

endlocal