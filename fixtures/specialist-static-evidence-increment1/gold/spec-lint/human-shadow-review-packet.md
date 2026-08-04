# SPEC-LINT Human Shadow Review Packet

Reviewability: **ready_for_human_shadow_review**

Comparison-only calibration; no admission, scheduling, report, deployment, or A100 authority.

## ITEM-0001 — observation

The project declares a repository-check command and implements a text-integrity rule function.

- `pyproject.toml` line 18: `harness-check = "code_harness.cli:check_repository"`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `tools/check_repository_structure.py` line 38: `def check_utf8_and_mojibake(errors: list[str]) -> None:`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

## ITEM-0002 — finding

No completed checker execution result is admitted for this candidate evidence population.

- `pyproject.toml` line 18: `harness-check = "code_harness.cli:check_repository"`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `tools/check_repository_structure.py` line 38: `def check_utf8_and_mojibake(errors: list[str]) -> None:`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

## ITEM-0003 — recommendation

Execute the pinned checker against the immutable revision and retain its source population, exit code, and output.

- `pyproject.toml` line 18: `harness-check = "code_harness.cli:check_repository"`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `tools/check_repository_structure.py` line 38: `def check_utf8_and_mojibake(errors: list[str]) -> None:`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

## ITEM-0004 — unknown

Rule execution coverage, violations, suppressions, false positives, complexity, and trend are unknown without a completed result.

- `pyproject.toml` line 18: `harness-check = "code_harness.cli:check_repository"`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

- `tools/check_repository_structure.py` line 38: `def check_utf8_and_mojibake(errors: list[str]) -> None:`
- Revision: `ada870cc7fc557a417f4215c8e60fbf3bee367d9`

