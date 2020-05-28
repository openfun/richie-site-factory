provider "aws" {
  alias = "virginia"
  region = "us-east-1"
}

resource "aws_acm_certificate" "certificate" {
  domain_name       = "${lookup(var.storage_domain, terraform.workspace)}"
  provider = "aws.virginia"
  validation_method = "DNS"

  tags = {
    Environment = "${terraform.workspace}"
    Customer = "fun"
  }

  lifecycle {
    create_before_destroy = true
  }
}

locals {
  s3_static_origin_id = "funmooc-static-origin"
  s3_media_origin_id = "funmooc-media-origin"
}

# Create an origin access identity that will allow CloudFront to access S3
# See bucket policies in s3.tf or documentation for more details:
# https://www.terraform.io/docs/providers/aws/r/cloudfront_origin_access_identity.html
resource "aws_cloudfront_origin_access_identity" "funmooc_oai" {
  comment = "fun-mooc origin for the ${terraform.workspace} environment"
}

resource "aws_cloudfront_distribution" "funmooc_cloudfront_distribution" {
  # Origin pointing to static files
  origin {
    domain_name = "${lookup(var.app_domain, terraform.workspace)}"
    origin_id   = "${local.s3_static_origin_id}"

    custom_origin_config {
      http_port = 80
      https_port = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols = ["SSLv3", "TLSv1", "TLSv1.1", "TLSv1.2"]
    }
  }

  # Origin for the media S3 bucket
  origin {
    domain_name = "${aws_s3_bucket.funmooc_media.bucket_domain_name}"
    origin_id   = "${local.s3_media_origin_id}"

    s3_origin_config {
      origin_access_identity = "${aws_cloudfront_origin_access_identity.funmooc_oai.cloudfront_access_identity_path}"
    }
  }

  enabled         = true
  is_ipv6_enabled = true
  aliases = ["${lookup(var.storage_domain, terraform.workspace)}"]

  # Allow public access by default, served by static bucket
  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "${local.s3_static_origin_id}"

    forwarded_values {
      query_string = false
      headers = ["Access-Control-Request-Headers", "Access-Control-Request-Method", "Authorization", "Origin"]

      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  # Media bucket: allow public access
  ordered_cache_behavior {
    path_pattern     = "/media/*"
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "${local.s3_media_origin_id}"

    forwarded_values {
      query_string = false
      headers = ["Access-Control-Request-Headers", "Access-Control-Request-Method", "Authorization", "Origin"]

      cookies {
        forward = "none"
      }
    }

    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
    compress               = true
    viewer_protocol_policy = "redirect-to-https"
  }

  price_class = "${lookup(var.cloudfront_price_class, terraform.workspace, "PriceClass_100")}"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  tags = {
    Environment = "${terraform.workspace}"
  }

  viewer_certificate {
    acm_certificate_arn = "${aws_acm_certificate.certificate.arn}"
    ssl_support_method = "sni-only"
  }
}
