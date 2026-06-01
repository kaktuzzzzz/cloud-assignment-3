output "alb_hostname" {
  value = aws_lb.main.dns_name
}
output "ecr_repository_url" {
  value = aws_ecr_repository.app.repository_url
}
output "cloudfront_domain_name" {
  value = aws_cloudfront_distribution.main.domain_name
}
