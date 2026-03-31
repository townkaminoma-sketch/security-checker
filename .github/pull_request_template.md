# Pull Request

## Background
Why is this checkpoint needed now?

## Purpose
What does this PR achieve?

## Non-goals
What is explicitly out of scope for this PR?

## Checkpoint
Which checkpoint does this PR correspond to?

## Changes
Summarize the actual changes.

## Changed files
List the files changed in this PR.
（Issue の Expected files と突き合わせる）

## Explicitly unaffected areas
List areas that were not changed.

## Test results
List only the tests and checks that were actually run.
Anything not run: write **not run** (do not imply done).

- Tests run:
- Lint run:
- Type checks run:
- CI status:

## Known trade-offs
What was intentionally accepted or left simple?

## Deferred improvements
What improvements were noticed but intentionally not included in this PR?

## Rollback plan
How can this PR be safely rolled back?
（対象外変更が混ざっていないか。1 手で説明できるか）

## AI self-check
- Stayed within one checkpoint:
- Avoided unrelated changes:
- Avoided broad refactor:
- Reported tests honestly:
- Changed files match the Issue expected surface (or Issue updated / explained):
- For docs-only / workflow-only / config-only checkpoints: no out-of-scope paths:
- Rollback is straightforward:

## Review focus
### ChatGPT review focus
- Purpose alignment
- Non-goal intrusion
- Checkpoint boundary

### Claude review focus
- Technical correctness
- Edge cases
- Security
- Performance
- Maintainability
- Rollback safety

### Human review focus
- Business value
- UX / operations fit
- Final adopt / hold decision
