module "service" {
  source = "git@github.com:trade-tariff/trade-tariff-platform-terraform-modules.git//aws/ecs-service?ref=aws/ecs-service-v1.11.3"

  region = var.region

  service_name  = local.service
  service_count = var.service_count

  cluster_name              = "trade-tariff-cluster-${var.environment}"
  subnet_ids                = data.aws_subnets.private.ids
  security_groups           = [data.aws_security_group.this.id]
  target_group_arn          = data.aws_lb_target_group.this.arn
  cloudwatch_log_group_name = "platform-logs-${var.environment}"

  min_capacity = var.min_capacity
  max_capacity = var.max_capacity

  docker_image = data.aws_ssm_parameter.ecr_url.value
  docker_tag   = var.docker_tag
  skip_destroy = true

  container_port = 8080

  cpu    = var.cpu
  memory = var.memory

  task_role_policy_arns = [
    aws_iam_policy.buckets.arn,
  ]

  execution_role_policy_arns = [
    aws_iam_policy.secrets.arn
  ]


  private_dns_namespace = "tariff.internal"

  service_environment_config = [
    {
      name  = "ENABLE_JSON_LOGGING"
      value = "true"
    },
    {
      name  = "EXPAND_EQUIVALENT_SYNONYMS"
      value = "false"
    },
    {
      name  = "EXPAND_EXPLICIT_SYNONYMS"
      value = "true"
    },
    {
      name  = "FLASK_APP"
      value = "flaskr"
    },
    {
      name = "FLASK_ENV"
      name = "production"
    },
    {
      name  = "MAXIMUM_WORD_LENGTH"
      value = 15
    },
    {
      name  = "PACKAGE_BUCKET_NAME"
      value = data.aws_s3_bucket.synonym_packages.bucket
    },
    {
      name  = "SPACY_DICTIONARY"
      value = "en_core_web_md"
    },
    {
      name  = "SPELLING_CORRECTOR_BUCKET_NAME"
      value = data.aws_s3_bucket.spelling_corrector.bucket
    },
    {
      name  = "SENTRY_ENVIRONMENT"
      value = var.environment
    },
  ]

  service_secrets_config = [
    {
      name      = "SENTRY_DSN"
      valueFrom = data.aws_secretsmanager_secret.sentry_dsn.arn
    },
  ]
}
