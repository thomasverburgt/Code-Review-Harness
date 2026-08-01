# Expert Evidence Annex

Report package: `43ac6c58-2d9f-5465-91a5-b7ac00e75e8f`
Report hash: `sha256:430233c423d65642bdebde1d9217517d7023bc2ddcc5dbbf89ebe361d9ceeb4a`
Reviewability: **ready_for_expert_review**

This annex supports human review only. It does not approve distribution, decide a finding, accept risk, or authorize a change.

## FINDING:SPEC-SECRETS:FINDING-001

A redacted credential-like value was detected in a documentation file, but its status as a confirmed secret is unresolved.

Reviewability: `ready`

- Evidence: `UDS-0001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.

## FINDING:PROD-SEC:FINDING-001

A redacted credential-like value was detected in a documentation file, but its status as a confirmed secret is unresolved.

Reviewability: `ready`

- Evidence: `UDS-0001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.

## FINDING:CAP-RISK:FINDING-001

A redacted credential-like value was detected in a documentation file, but its status as a confirmed secret is unresolved.

Reviewability: `ready`

- Evidence: `UDS-0001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.

## FINDING:ENT-SYSRISK:FINDING-001

A redacted credential-like value was detected in a documentation file, but its status as a confirmed secret is unresolved.

Reviewability: `ready`

- Evidence: `OBS-RISK-001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.

## RISK:RISK-001

A redacted credential-like value was detected in a documentation file, but its status as a confirmed secret is unresolved.

Reviewability: `ready`

- Evidence: `OBS-RISK-001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.

## CAPA:a5d58ea0-6ce4-5b93-967a-7de957ce0655

Classify the redacted value as confirmed secret, likely secret, or benign/nonsecret. Implement a process to ensure that documentation files do not contain credential-like values.

Reviewability: `ready`

- Evidence: `UDS-0001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.

## RECOMMENDATION:487ad1d4-9f67-56aa-a0b6-91e41f9f3664

Classify the redacted value as confirmed secret, likely secret, or benign/nonsecret.

Reviewability: `ready`

- Evidence: `UDS-0001`
- Repository: `https://github.com/defenseunicorns/uds-core.git`
- Immutable revision: `329ade01852f9e570d31cb7b19d9979152938c17`
- File: `docs/getting-started/local-demo/integrate-your-package.mdx` (lines 153-153)
- Safe excerpt: Credential-like assignment detected; matched value omitted.
- Fingerprint: `sha256:411fdec1c7f0f0ada4b089edf43886b0aafc6fb59d7df8ad434363c469a58bca`
- Reviewer reproduction:
  1. Check out commit 329ade01852f9e570d31cb7b19d9979152938c17 from https://github.com/defenseunicorns/uds-core.git.
  2. Open docs/getting-started/local-demo/integrate-your-package.mdx at line 153.
  3. Run the approved redacted credential-assignment check and compare the line fingerprint.
