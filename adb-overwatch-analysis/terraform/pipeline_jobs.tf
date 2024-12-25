resource "databricks_job" "load_lakedata" {
  name = "Load Lake Data Job"

    task {
    task_key = "load_lakedata_task"
    notebook_task {
       notebook_path = "/Workspace/Overwatch/Analysis/Load to bronze"
    }
    
    new_cluster {
    spark_version = "7.3.x-scala2.12"
    node_type_id  = "Standard_D4ds_v5"
    num_workers   = 2
    ssh_public_keys = []
    custom_tags = {}
    spark_env_vars = {
      PYSPARK_PYTHON = "/databricks/python3/bin/python3"
    }
    enable_elastic_disk = true
  }
  }

  schedule {
    quartz_cron_expression = "0 0 * * * ?"  # Daily at midnight
    timezone_id            = "UTC"
  }
}

# Resource pipeline names and description
resource "databricks_job" "load_lakedata_second" {
  name = "Load Lake Data Job second"

    task {
    task_key = "load_lakedata_task2"
    notebook_task {
       notebook_path = "/Workspace/Overwatch/Analysis/Load to bronze"
    }
    
    new_cluster {
    spark_version = "7.3.x-scala2.12"
    node_type_id  = "Standard_D4ds_v5"
    num_workers   = 2
    ssh_public_keys = []
    custom_tags = {}
    spark_env_vars = {
      PYSPARK_PYTHON = "/databricks/python3/bin/python3"
    }
    enable_elastic_disk = true
  }
  }

  schedule {
    quartz_cron_expression = "0 0 * * * ?"  # Daily at midnight
    timezone_id            = "UTC"
  }
}