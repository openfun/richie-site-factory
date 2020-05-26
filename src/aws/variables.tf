
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

variable "app_domain" {
  type = "map"

  default = {
    production = "www.fun-mooc.fr"
    preprod = "preprod.fun.oc.openfun.fr"
    staging = "staging.fun.oc.openfun.fr"
  }
}
