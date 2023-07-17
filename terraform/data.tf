data "aws_caller_identity" "current" {}

data "aws_vpc" "vpc" {
  tags = { Name = "trade_tariff_${var.environment}_vpc" }
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
  name = "trade-tariff-sqp-tg-${var.environment}"
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
