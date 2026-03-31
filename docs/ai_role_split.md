# AI role split guide

## Purpose

Fix the working role split for this repository so that checkpoint work stays small, reviewable, and approval-driven.

This document is operational guidance.
It does not change implementation behavior by itself.

## Role split

### Claude Code

Primary use:
- read the repo
- inspect PRs and Issues through `gh`
- produce implementation plans
- analyze review points and technical risks

Typical outputs:
- small implementation plan
- changed / non-changed file expectations
- technical risk notes
- review checklist draft

### Claude (browser)

Primary use:
- polish review text
- refine wording for Issues / PRs / comments
- discuss design alternatives

Typical outputs:
- review comment drafts
- issue / PR body drafts
- wording cleanup
- design discussion notes

### Cursor / Codex

Primary use:
- implement approved small diffs
- commit changes
- open PRs
- perform small follow-up edits

Typical outputs:
- code changes
- tests for the changed boundary
- commit message
- PR body

### ChatGPT

Primary use:
- fix purpose and scope
- judge mainline priority
- design the next checkpoint
- organize merge judgment
- act as the overall gate for route discipline

Typical outputs:
- checkpoint definition
- scope / non-scope review
- mainline vs hold-lane judgment
- merge recommendation framing
- next-slice proposal

### GitHub UI

Primary use:
- final checks confirmation
- manual merge

### Human

Primary use:
- adoption judgment
- final approval to merge
- hold / rollback decisions when needed

## Working rules

- 1 Issue = 1 checkpoint
- 1 PR = 1 purpose
- minimal diff only
- if CI fails, do not merge
- keep mainline narrow
- keep PR #10 and Tiingo work on separate lanes unless explicitly re-scoped

## Recommended working flow

1. ChatGPT fixes the checkpoint purpose and scope.
2. Claude Code reads the repo and proposes the smallest plan.
3. Human approves the plan.
4. Cursor / Codex implements the approved small diff.
5. Claude (browser) may help polish issue / PR / review text.
6. ChatGPT reviews route fit, scope discipline, and merge framing.
7. GitHub UI is used for final checks confirmation and manual merge.
8. Human makes the final adoption decision.

## Non-goals

- do not let multiple tools independently drive mainline priorities
- do not treat browser Claude as the main GitHub source of truth
- do not remove human approval from merge decisions
- do not expand one checkpoint into multiple purposes

## Notes

This split is intended to reduce role collision and keep checkpoint work approval-driven.
If the split stops serving that goal, it should be revised by a separate checkpoint.
