data "aws_iam_policy_document" "buckets" {
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:ListBucket"
    ]
    resources = [
      data.aws_s3_bucket.synonym_packages.arn,
      "${data.aws_s3_bucket.synonym_packages.arn}/config/opensearch/stemming_exclusions_all.txt",
      "${data.aws_s3_bucket.synonym_packages.arn}/config/opensearch/synonyms_all.txt",
      data.aws_s3_bucket.spelling_corrector.arn,
      "${data.aws_s3_bucket.spelling_corrector.arn}/spelling-corrector/spelling-model.txt",
    ]
  }

  statement {
    effect    = "Allow"
    actions   = ["kms:Decrypt"]
    resources = [data.aws_kms_key.opensearch_key.arn]
  }
}

data "aws_iam_policy_document" "secrets" {
  statement {
    effect = "Allow"
    actions = [
      "secretsmanager:GetResourcePolicy",
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
      "secretsmanager:ListSecretVersionIds"
    ]
    resources = [
      data.aws_secretsmanager_secret.sentry_dsn.arn
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "kms:Encrypt",
      "kms:Decrypt",
      "kms:ReEncryptFrom",
      "kms:ReEncryptTo",
      "kms:GenerateDataKeyPair",
      "kms:GenerateDataKeyPairWithoutPlainText",
      "kms:GenerateDataKeyWithoutPlaintext"
    ]
    resources = [
      data.aws_kms_key.secretsmanager_key.arn
    ]
  }
}

resource "aws_iam_policy" "buckets" {
  name   = "${local.service}-execution-role-buckets-policy"
  policy = data.aws_iam_policy_document.buckets.json
}

resource "aws_iam_policy" "secrets" {
  name   = "searcy-query-parser-execution-role-secrets-policy"
  policy = data.aws_iam_policy_document.secrets.json
}
