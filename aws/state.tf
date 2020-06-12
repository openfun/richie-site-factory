terraform {
  backend "s3" {
    encrypt = true
    bucket = "richie-site-factory-terraform"
    dynamodb_table = "richie_site_factory_terraform_state_locks"
  }
}
