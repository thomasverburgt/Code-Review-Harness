# SPEC-SBOM Human Shadow Review Packet

Reviewability: **ready_for_human_shadow_review**

Comparison-only calibration; no admission, scheduling, report, deployment, or A100 authority.

## ITEM-0001 — observation

The manifest declares setuptools and python-docx components for the bounded source population.

- `pyproject.toml` line 2: `requires = ["setuptools"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `pyproject.toml` line 15: `docs = ["python-docx==1.2.0"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

## ITEM-0002 — finding

The admitted evidence contains declarations but no resolved, artifact-derived, or signed SBOM inventory.

- `pyproject.toml` line 2: `requires = ["setuptools"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `pyproject.toml` line 15: `docs = ["python-docx==1.2.0"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

## ITEM-0003 — recommendation

Generate a content-addressed SBOM from the resolved build and retain its method and source population.

- `pyproject.toml` line 2: `requires = ["setuptools"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `pyproject.toml` line 15: `docs = ["python-docx==1.2.0"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

## ITEM-0004 — unknown

Transitive components, artifact contents, suppliers, package identifiers, and runtime inventory are unknown.

- `pyproject.toml` line 2: `requires = ["setuptools"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `pyproject.toml` line 15: `docs = ["python-docx==1.2.0"]`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

