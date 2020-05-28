
variable "aws_region" {
  type    = "string"
  default = "eu-west-1"
}

variable "cloudfront_price_class" {
  type = "map"

  default = {
    production = "PriceClass_All"
  }
}

variable "storage_domain" {
  type = "map"

  default = {
    production = "storage.fun-mooc.fr"
    preprod = "storage-preprod.fun-mooc.fr"
    staging = "storage-staging.fun-mooc.fr"
  }
}

variable "app_domain" {
  type = "map"

  default = {
    production = "new.fun-mooc.fr"
    preprod = "preprod.fun.oc.openfun.fr"
    staging = "staging.fun.oc.openfun.fr"
  }
}
