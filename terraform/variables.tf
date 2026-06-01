variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}
variable "project_name" {
  description = "Project name for resource tagging"
  default     = "nguyenpanda-fargate"
}
variable "vpc_cidr" {
  description = "CIDR block for VPC"
  default     = "10.0.0.0/16"
}
variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}
variable "container_port" {
  description = "Port exposed by the docker image"
  default     = 8000
}
variable "cpu" {
  description = "Fargate instance CPU units"
  default     = "256"
}
variable "memory" {
  description = "Fargate instance memory"
  default     = "512"
}
variable "desired_count" {
  description = "Number of docker containers to run"
  default     = 2
}
variable "domain_name" {
  description = "Custom domain name"
  default     = ""
}
