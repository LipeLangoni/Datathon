provider "aws" {
  region = "us-east-1"  
}
data "aws_ecr_repository" "lambda_repository" {
  name = "lambda-repo" 
}

resource "aws_lambda_function" "lambda_function" {
  function_name = "my-lambda-function"
  s3_bucket     = aws_s3_bucket.lambda_s3_bucket.bucket
  s3_key        = "lambda-code.zip"
  handler       = "index.handler"
  runtime       = "nodejs14.x"
  role          = aws_iam_role.lambda_exec_role.arn
}
