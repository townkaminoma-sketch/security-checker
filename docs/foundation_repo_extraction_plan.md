# Foundation repo extraction plan

## Purpose

Define a low-risk path for evolving `python-template` into a clearer split between:

- a reusable foundation repo for checkpoint-gated AI-assisted development
- a product / research repo that keeps domain-specific logic

This document does **not** perform the split yet.
It fixes the intended order, boundaries, and guardrails first.

## Current working approach

The repository is currently acting as a **candidate foundation host**.
Recent work has shown that small, reviewable checkpoints can land cleanly on `main`.
That working flow should continue before extracting a separate foundation repo.

## Planned order

### Phase 1: keep growing `python-template` as a candidate foundation host

Use the current repository to keep stabilizing:

- checkpoint state handling
- issue / PR contracts
- narrow scope enforcement
- rollback-friendly PR shapes
- deterministic evidence and honest check reporting

During this phase:

- continue the small Checkpoint 1 mainline slices
- keep PR #10 on a separate holding lane
- keep PR #14 on a separate holding lane
- do not begin broad repo splitting work

### Phase 2: define the extraction boundary explicitly (DONE — CP1)

Boundary is now defined in `docs/foundation_boundary.md`. Summary below.

#### Foundation layer (stays in template)

- `.github/` — workflows (`ci.yml`, `pr-invariants.yml`), ISSUE_TEMPLATE, PR template
- `scripts/check_pr_invariants.py` — PR scope enforcement
- `docs/` — checkpoint 運用系のみ (`checkpoint_state_machine.md`, `claude_checkpoint_workflow.md`, `ai_role_split.md`, `foundation_boundary.md`, `foundation_repo_extraction_plan.md`)
- root files — `CLAUDE.md`, `AGENTS.md`, `PLAN.md`, `README.md`, `SPEC.md`
- dev config — `pyproject.toml` (dev deps only), `.pre-commit-config.yaml`, `.editorconfig`, `.gitignore`, `.gitattributes`, `.mcp.json`
- directory skeleton — empty `src/`, `tests/`, `scripts/`

#### Product / research layer (moves to app repo)

- `src/investment_system/` — all domain modules (backtest, signals, portfolio, risk, etc.)
- `src/main.py` — domain entry point
- `configs/*.json` — strategy parameters
- `data/`, `outputs/` — domain data and generated outputs
- `scripts/` — domain scripts (build_real_data_csv, fetch_*, view_*, run_*, checkpoint001_emit_*)
- `tests/` — all domain tests (test_checkpoint*, test_orchestration, test_improvement_*, etc.)
- `docs/` — domain docs (strategy_comparison_summary, checkpoint_002_issue, multi_ai_*, draft_issue_*)
- `package.json` — domain-specific

#### Boundary decision criteria

See `docs/foundation_boundary.md` for the full rationale and file-by-file classification.

### Phase 3: create a separate foundation repo

After the boundary is stable, create a separate foundation repo that contains only the reusable checkpoint-development operating system.

That repo should stay intentionally light.
It should not absorb product logic, research results, or domain-specific behavior.

### Phase 4: start future systems from the foundation repo

After the separate foundation repo exists and is validated, use it as the starting point for new systems.

`python-template` can then remain focused on its current product / research role, while the foundation repo serves as the reusable base.

## Rules for this route

- 1 Issue = 1 checkpoint
- 1 PR = 1 purpose
- minimal diff only
- if CI fails, do not merge
- do not mix repo-foundation work with PR #10 or Tiingo work
- do not extract product-specific logic into the foundation repo

## Near-term next actions

1. review and merge the current small Checkpoint 1 PRs only when checks are green
2. continue small Checkpoint 1 slices on `main`
3. use later checkpoints to clarify foundation vs product boundaries if needed
4. only then create the separate foundation repo

## Non-goals

- no immediate multi-repo migration
- no broad reorganization of `src/`
- no orchestrator revival through this plan
- no Tiingo workflow expansion through this plan
- no immediate replacement of the current repository
