data "aws_iam_policy_document" "buckets" {
  statement {
    effect  = "Allow"
    actions = ["s3:GetObject"]
    resources = [
      data.aws_s3_bucket.synonym_packages.arn,
      "${data.aws_s3_bucket.synonym_packages.arn}/config/opensearch/stemming_exclusions_all.txt",
      "${data.aws_s3_bucket.synonym_packages.arn}/config/opensearch/synonyms_all.txt",
      data.aws_s3_bucket.spelling_corrector.arn,
      "${data.aws_s3_bucket.spelling_corrector.arn}/spelling-corrector/spelling-model.txt",
    ]
  }
}

resource "aws_iam_policy" "buckets" {
  name   = "${local.service}-execution-role-buckets-policy"
  policy = data.aws_iam_policy_document.buckets.json
}
