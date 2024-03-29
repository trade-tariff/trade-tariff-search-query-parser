data "aws_caller_identity" "current" {}

data "aws_vpc" "vpc" {
  tags = { Name = "trade-tariff-${var.environment}-vpc" }
}

data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.vpc.id]
  }

  tags = {
    Name = "*private*"
  }
}

data "aws_lb_target_group" "this" {
  name = "search-query-parser"
}

data "aws_security_group" "this" {
  name = "trade-tariff-ecs-security-group-${var.environment}"
}

data "aws_ssm_parameter" "ecr_url" {
  name = "/${var.environment}/SEARCH_QUERY_PARSER_ECR_URL"
}

data "aws_s3_bucket" "spelling_corrector" {
  bucket = "trade-tariff-search-configuration-${local.account_id}"
}

data "aws_s3_bucket" "synonym_packages" {
  bucket = "trade-tariff-opensearch-packages-${local.account_id}"
}

data "aws_kms_key" "opensearch_key" {
  key_id = "alias/opensearch-key"
}

data "aws_secretsmanager_secret" "sentry_dsn" {
  name = "search-query-parser-sentry-dsn"
}

data "aws_kms_key" "secretsmanager_key" {
  key_id = "alias/secretsmanager-key"
}
