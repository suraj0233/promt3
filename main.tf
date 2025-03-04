# aws_integration.tf
terraform {
  required_providers {
    spacelift = {
      source = "spacelift-io/spacelift"
    }
  }
}

# AWS Integration for Spacelift
resource "spacelift_aws_integration" "developer_account" {
  name            = "developer-${var.aws_account_id}"
  role_arn        = "arn:aws:iam::${var.aws_account_id}:role/Spacelift"
  description     = "AWS integration for developer account ${var.aws_account_id}"
  generate_credentials_in_spacelift = false
}

# Variables
variable "aws_account_id" {
  description = "AWS Account ID to integrate with Spacelift"
  type        = string
}
