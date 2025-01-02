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
  host  = "https://adb-.azuredatabricks.net"
  token = "XXXXX"
}
