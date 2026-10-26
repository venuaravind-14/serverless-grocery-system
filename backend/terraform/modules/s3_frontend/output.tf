output "bucket_name" {
  value = aws_s3_bucket.frontend.id
}

output "website_endpoint" {
  value = "http://${aws_s3_bucket_website_configuration.frontend_website.website_endpoint}"
}
