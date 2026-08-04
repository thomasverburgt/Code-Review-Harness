# SPEC-COMMS Deferred Human Shadow Review Packet

Reviewability: **ready_for_human_shadow_review**

Retained for consolidated end-of-program human review. Comparison-only; no admission, scheduling, report, deployment, or A100 authority.

## ITEM-0001 - observation

The topology declares an exposed httpbin service and egress, while communication policy declares STRICT mTLS with a port-specific PERMISSIVE exception and documents that UDP bypasses Istio mTLS and AuthorizationPolicy.

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 12: `    mode: STRICT`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 19: `      mode: PERMISSIVE`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/test/app-admin-package.yaml` line 17: `        - name: httpbin`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0002 - finding

No rendered route set, identity binding, authorization result, traffic test, telemetry, or failure-path evidence is admitted.

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 12: `    mode: STRICT`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 19: `      mode: PERMISSIVE`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/test/app-admin-package.yaml` line 17: `        - name: httpbin`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0003 - recommendation

Retain the rendered topology plus authenticated positive and unauthorized negative traffic tests for every declared path and exception.

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 12: `    mode: STRICT`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 19: `      mode: PERMISSIVE`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/test/app-admin-package.yaml` line 17: `        - name: httpbin`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

## ITEM-0004 - unknown

Effective identity, encryption, authorization, exposure, lateral-movement resistance, and failure behavior are not demonstrated without runtime traffic evidence.

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 12: `    mode: STRICT`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/metrics-server/chart/templates/peerauthentication/metrics-api.yaml` line 19: `      mode: PERMISSIVE`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/pepr/operator/crd/sources/package/v1alpha1.ts` line 185: `UDP traffic is not protected by Istio AuthorizationPolicy or mTLS.`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

- `src/test/app-admin-package.yaml` line 17: `        - name: httpbin`
- Revision: `329ade01852f9e570d31cb7b19d9979152938c17`

