---
name: review-iac-diff
description: Review an infrastructure-as-code change (CDK diff, Terraform plan, CloudFormation change set) and summarize created, changed, replaced and destroyed resources and risks. Use before applying infrastructure changes.
---

# review-iac-diff

Make a plan/diff reviewable. This skill **reads and explains; it never applies, deploys or destroys.**

**Inputs:** a plan/diff (pasted, a file, or produce one with a read-only command: `cdk diff`, `terraform plan -out=… && terraform show`, `aws cloudformation describe-change-set`). If producing it requires credentials the user hasn't configured, ask.
**Output:** a review summary.

## Procedure

1. **Obtain the diff** using read-only commands only. State which stack/workspace/account it is for.
2. **Inventory** every resource into one of: **create**, **update in place**, **replace** (destroy + create), **destroy**. Replacements and destroys are the headline.
3. **Flag stateful resources** affected by replace/destroy: databases, buckets, queues, volumes, KMS keys, log groups, DNS records. State whether data would be lost and whether the resource has a retention/removal policy.
4. **Security review of what changes:**
   - IAM: `*` actions or `*` resources, new trust relationships, privilege escalation paths, loss of conditions.
   - Network: new `0.0.0.0/0` ingress, public subnets/IPs, public buckets or endpoints.
   - Encryption: encryption turned off or changed, new unencrypted resources.
   - Logging/monitoring removed.
5. **Cost and blast radius:** large instance types, NAT gateways, cross-region replication, anything that scales with traffic.
6. **Drift check:** note changes the user did not intend (resources that show up changed with no matching code change).

## Output format

```
## Target
<account / region / stack or workspace>

## Headline
<one sentence: safe / needs attention / do not apply>

## Replace / destroy
- <resource> — <why> — data loss? <yes/no/unknown>

## Create / update
<grouped list>

## Security findings
- [HIGH|MED|LOW] <finding> — <resource>

## Questions before applying
- ...
```

## Rules

- Never run `apply`, `deploy`, `destroy` or `import`.
- If the diff is truncated or unparseable, say so rather than summarizing what you can see.
- Treat an unexpected replacement of a stateful resource as blocking until the user explains it.
