output "api_gateway_url" {
  value       = module.api_gateway.api_gateway_url
  description = "Base URL of the Amazon API Gateway HTTP API"
}

output "frontend_bucket_name" {
  value       = module.s3_frontend.bucket_name
  description = "Name of the S3 bucket hosting the React frontend"
}

output "frontend_website_url" {
  value       = module.s3_frontend.website_endpoint
  description = "Public URL of the hosted React frontend on Amazon S3"
}
