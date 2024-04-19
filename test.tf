terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.9"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>4.0"
    }
  }
}

provider "azurerm" {
  features {}
}
