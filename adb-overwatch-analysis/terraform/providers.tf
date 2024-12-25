terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 2.0"
    }
    databricks = {
      source = "databricks/databricks"
      version = "~> 0.3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

provider "databricks" {
  host  = "https://adb-3510475013252491.11.azuredatabricks.net"
  token = "dapifb84297d915bf56e3d70661ccf0b988e-3"
}