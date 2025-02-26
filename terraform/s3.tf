resource "aws_s3_bucket" "lambda_s3_bucket" {
  bucket = "lambda-code-bucket"
}

output "lambda_function_name" {
  value = aws_lambda_function.lambda_function.function_name
}

output "s3_bucket_name" {
  value = aws_s3_bucket.lambda_s3_bucket.bucket
}

output "ecr_repository_url" {
  value = data.aws_ecr_repository.lambda_repository.repository_url