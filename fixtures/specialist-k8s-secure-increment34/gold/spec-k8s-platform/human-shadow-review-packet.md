# SPEC-K8S-PLATFORM Deferred Human Shadow Review Packet

Reviewability: **ready_for_human_shadow_review**

Retained for consolidated end-of-program human review. Comparison-only; no admission, scheduling, report, deployment, or A100 authority.

## ITEM-0001 - observation

The admitted EKS desired state enables the VPC CNI network-policy option.

- `.github/test-infra/aws/eks/cluster.tf` line 160: `        enableNetworkPolicy = "true"`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0002 - finding

No live cluster state, policy inventory, enforcement test, tenant boundary test, control-plane observation, or failure evidence is admitted.

- `.github/test-infra/aws/eks/cluster.tf` line 160: `        enableNetworkPolicy = "true"`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0003 - recommendation

Retain live configuration and negative/positive enforcement tests for the exact cluster revision.

- `.github/test-infra/aws/eks/cluster.tf` line 160: `        enableNetworkPolicy = "true"`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0004 - unknown

Actual installation, enforcement, coverage, tenant isolation, drift, and platform effectiveness remain unknown from IaC desired state alone.

- `.github/test-infra/aws/eks/cluster.tf` line 160: `        enableNetworkPolicy = "true"`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

