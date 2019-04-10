
terraform {
  backend "s3" {
    key            = "funmooc.tfstate"
    bucket         = "funmooc-terraform"
    dynamodb_table = "funmooc_terraform_state_locks"
    encrypt        = true
  }
}
