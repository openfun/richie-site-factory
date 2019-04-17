resource "aws_kms_key" "state_key" {
  description = "Used by Terraform to store remote state for the fun-mooc project"
}

resource "aws_s3_bucket" "state_bucket" {
  bucket = "funmooc-terraform"
  acl    = "private"
  region = "${var.aws_region}"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        kms_master_key_id = "${aws_kms_key.state_key.arn}"
        sse_algorithm     = "aws:kms"
      }
    }
  }

  tags {
    Name = "terraform"
  }
}
