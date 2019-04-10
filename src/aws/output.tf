output "cloudfront_domain" {
  value = "${aws_cloudfront_distribution.funmooc_cloudfront_distribution.domain_name}"
}

output "iam_access_key" {
  value = "${aws_iam_access_key.funmooc_access_key.id}"
}

output "iam_access_secret" {
  value = "${aws_iam_access_key.funmooc_access_key.secret}"
}
