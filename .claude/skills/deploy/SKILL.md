---
name: deploy
description: Deploy a static site or frontend build to S3 and invalidate CloudFront, with a dry run and explicit confirmation. Use only when the user explicitly asks to deploy.
disable-model-invocation: true
---

# deploy

Ship a static build to S3 + CloudFront safely. This changes a **live, shared system**, so it is user-invoked only and confirms before every write.

> **Prefer CI.** If the repo already deploys from CI (e.g. GitHub Actions with OIDC), tell the user to push/merge instead and stop. Deploying from a laptop bypasses review and leaves no audit trail.

> **Customize.** Set the `TODO(team)` values below before use.

**Inputs:** target environment (default: none — ask). Never assume production.
**Output:** a deployment report (what changed, where, invalidation ID, verification result, rollback path).
**Configuration:** `TODO(team)`: bucket per environment, CloudFront distribution ID per environment, build command, build output dir.

## Procedure

1. **Preconditions.** Confirm the working tree is clean (`git status`), the current branch is the expected release branch, and tests/lint pass. If not, stop and report.
2. **Build.** Run the build command; confirm the output directory is non-empty.
3. **Show what will change.** Run `aws s3 sync <dir> s3://<bucket> --delete --dryrun` and summarize: files added / changed / **deleted**. Call out any deletion that is not a build artifact.
4. **Confirm.** Show the target (account, bucket, distribution) and ask the user to approve, naming the environment explicitly. Do not proceed on silence or on a general "go ahead" given before the dry run.
5. **Deploy.** Run the sync for real. Set a short `Cache-Control` on HTML (e.g. `max-age=300`) and a long one on fingerprinted assets.
6. **Invalidate.** `aws cloudfront create-invalidation --distribution-id <id> --paths '/*'` (or only the changed paths).
7. **Verify.** Request the home page and one changed page; report the HTTP status. Report the invalidation ID.
8. **Report** what was deployed, where, and how to roll back.

## Rollback

Re-deploy the previous git tag/commit through the same steps. If the bucket is versioned, restore the previous object versions. Say which applies.

## Rules

- Never run with `--delete` without showing the dry run first.
- Never deploy from a dirty tree or an unexpected branch without explicit approval.
- Never print credentials; use the already-configured AWS profile/role.
- If the AWS identity is not the expected account, stop.
