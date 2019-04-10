# Create S3 Bucket for static files
resource "aws_s3_bucket" "funmooc_static" {
  bucket = "${terraform.workspace}-funmooc-static"
  acl    = "private"
  region = "${var.aws_region}"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    max_age_seconds = 3600
  }

  tags {
    Name        = "funmooc-static"
    Environment = "${terraform.workspace}"
  }
}

# Create S3 Bucket for media files
resource "aws_s3_bucket" "funmooc_media" {
  bucket = "${terraform.workspace}-funmooc-media"
  acl    = "private"
  region = "${var.aws_region}"

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET"]
    allowed_origins = ["*"]
    max_age_seconds = 3600
  }

  tags {
    Name        = "funmooc-media"
    Environment = "${terraform.workspace}"
  }
}

# Defines a user that should be able to write to both S3 buckets
resource "aws_iam_user" "funmooc_user" {
  name = "${terraform.workspace}-funmooc"
}

resource "aws_iam_access_key" "funmooc_access_key" {
  user = "${aws_iam_user.funmooc_user.name}"
}

# Grant accesses to the static bucket:
# - full access for the user,
# - read only access for CloudFront.
resource "aws_s3_bucket_policy" "funmooc_static_bucket_policy" {
  bucket = "${aws_s3_bucket.funmooc_static.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "User access",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_iam_user.funmooc_user.arn}"
      },
      "Action": [ "s3:*" ],
      "Resource": [
        "${aws_s3_bucket.funmooc_static.arn}",
        "${aws_s3_bucket.funmooc_static.arn}/*"
      ]
    },
    {
      "Sid": "Cloudfront",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_cloudfront_origin_access_identity.funmooc_oai.iam_arn}"
      },
      "Action": "s3:GetObject",
      "Resource": "${aws_s3_bucket.funmooc_static.arn}/*"
    }
  ]
}
EOF
}

# Grant accesses to the media bucket:
# - full access for the user,
# - read only access for CloudFront.
resource "aws_s3_bucket_policy" "funmooc_media_bucket_policy" {
  bucket = "${aws_s3_bucket.funmooc_media.id}"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "User access",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_iam_user.funmooc_user.arn}"
      },
      "Action": [ "s3:*" ],
      "Resource": [
        "${aws_s3_bucket.funmooc_media.arn}",
        "${aws_s3_bucket.funmooc_media.arn}/*"
      ]
    },
    {
      "Sid": "Cloudfront",
      "Effect": "Allow",
      "Principal": {
        "AWS": "${aws_cloudfront_origin_access_identity.funmooc_oai.iam_arn}"
      },
      "Action": "s3:GetObject",
      "Resource": "${aws_s3_bucket.funmooc_media.arn}/*"
    }
  ]
}
EOF
}
