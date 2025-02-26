resource "aws_security_group" "mlflow_sg" {
  name        = "mlflow-sg"
  description = "Allow HTTP traffic to MLflow"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all incoming traffic
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Allow all outgoing traffic
  }
}

resource "aws_lb_target_group_attachment" "mlflow_target_attachment" {
  target_group_arn = aws_lb_target_group.mlflow_target_group.arn
  target_id        = aws_ecs_service.mlflow_service.id
  port             = 5000
}
