# SPEC-INTEROP Deferred Human Shadow Review Packet

Reviewability: **ready_for_human_shadow_review**

Retained for consolidated end-of-program human review. Comparison-only; no admission, scheduling, report, deployment, or A100 authority.

## ITEM-0001 - observation

The admitted source contract distinguishes UDP routing, incompatible hostname fields, and its trust-control boundary.

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `          "The routing protocol for this expose entry. When set to `UDP`, the entry routes through Envoy Gateway instead of Istio. Hostname routing fields (`host`, `domain`, `advancedHTTP`, `match`) are invalid for UDP entries. UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.",`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0002 - finding

A declared interface contract does not demonstrate producer-consumer compatibility, version negotiation, or live integration behavior.

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `          "The routing protocol for this expose entry. When set to `UDP`, the entry routes through Envoy Gateway instead of Istio. Hostname routing fields (`host`, `domain`, `advancedHTTP`, `match`) are invalid for UDP entries. UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.",`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0003 - recommendation

Retain versioned producer and consumer contracts plus compatibility and failure-path tests.

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `          "The routing protocol for this expose entry. When set to `UDP`, the entry routes through Envoy Gateway instead of Istio. Hostname routing fields (`host`, `domain`, `advancedHTTP`, `match`) are invalid for UDP entries. UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.",`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0004 - unknown

Consumer population, version compatibility, error semantics, and runtime integration remain unknown.

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `          "The routing protocol for this expose entry. When set to `UDP`, the entry routes through Envoy Gateway instead of Istio. Hostname routing fields (`host`, `domain`, `advancedHTTP`, `match`) are invalid for UDP entries. UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.",`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

