data "azurerm_resource_group" "rg" {
  name = var.rg_name
}

data "azurerm_databricks_workspace" "adb-ws" {
  name                = var.overwatch_ws_name
  resource_group_name = var.rg_name
}

//Upload Databricks notebooks used to analyse the Overwatch results
resource "databricks_notebook" "overwatch_analysis" {
  for_each = toset(["Load to bronze"])
  source   = "${path.module}/src/notebooks/${each.key}.py"
  path     = "/Overwatch/Analysis/${each.key}"
#  format   = "SOURCE"
  language = "PYTHON"
}