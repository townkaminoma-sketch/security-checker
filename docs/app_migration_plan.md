# App 分離移行計画

## 概要

`python-template` から投資システム固有のコードを `app-investment` repo に分離し、
`python-template` を foundation-template として完成させるための移行計画。

## 依存分析の結果

### 内部依存グラフ（src/investment_system/）

循環依存なし。クリーンな非循環グラフ。

```
shared_foundation.py ─────────────────────────────────┐
checkpoint1_audit.py ──────────────────────────────┐   │
                                                   ↓   ↓
data_loader.py ──────┐   config.py ◄──── checkpoint1_audit
                     ↓        ↓
              signals.py   risk.py
                  ↓    ↓      ↓
              portfolio.py ◄──┘
                  ↓
backtest.py ◄─────┘
    ↓
compare.py
report.py

horizon_skeletons.py ◄── shared_foundation
checkpoint1_lineup.py ◄── horizon_skeletons, shared_foundation
checkpoint1_context.py ◄── checkpoint1_lineup, horizon_skeletons, shared_foundation
checkpoint1_runner.py ◄── checkpoint1_io, config, data_loader, signals, shared_foundation
checkpoint2_runner.py ◄── backtest, config, data_loader, shared_foundation
checkpoint3_compare.py ◄── backtest, shared_foundation

cli.py ◄── backtest, compare, config, data_loader, portfolio, report, risk, signals
orchestration.py （内部依存なし、自己完結）
```

### 外部依存

- サードパーティ依存: **ゼロ**（標準ライブラリのみ）
- 本番依存パッケージ: なし（pyproject.toml の dependencies = []）

### 硬直パス参照

- `backtest.py`: `data/official/fred_dgs10.csv`, `data/official/treasury_avg_interest_rate.csv`, `data/official/treasury_certified_10y.csv`
- `scripts/build_real_data_csv.py`: `data/etf_universe_2013_2026.csv`
- `scripts/refresh_mainline_monitoring.py`: `configs/default.json`, `configs/default_walkforward.json`, 他

これらは app-investment にそのまま移動すれば動作する（相対パス基準が repo root のため）。

---

## 移動対象ファイル

### app-investment に移すもの

#### ソースコード
- `src/investment_system/` — 全20モジュール
  - `__init__.py`, `backtest.py`, `checkpoint1_audit.py`, `checkpoint1_context.py`
  - `checkpoint1_io.py`, `checkpoint1_lineup.py`, `checkpoint1_runner.py`
  - `checkpoint2_runner.py`, `checkpoint3_compare.py`, `cli.py`
  - `compare.py`, `config.py`, `data_loader.py`, `horizon_skeletons.py`
  - `orchestration.py`, `portfolio.py`, `report.py`, `risk.py`
  - `shared_foundation.py`, `signals.py`
- `src/investment_system/orchestrator/` — サブパッケージ全体
- `src/main.py` — エントリポイント

#### テスト
- `tests/test_checkpoint1_audit.py`
- `tests/test_checkpoint1_cli_slice.py`
- `tests/test_checkpoint1_config_audit.py`
- `tests/test_checkpoint1_context.py`
- `tests/test_checkpoint1_foundation_skeleton.py`
- `tests/test_checkpoint1_io.py`
- `tests/test_checkpoint1_lineup.py`
- `tests/test_checkpoint1_runner.py`
- `tests/test_checkpoint2_runner.py`
- `tests/test_checkpoint3_compare.py`
- `tests/test_cli_checkpoint1_horizons.py`
- `tests/test_orchestration.py`
- `tests/test_improvement_auto_continue_script.py`
- `tests/test_improvement_auto_continue_summary_script.py`
- `tests/test_improvement_handoff_view_script.py`
- `tests/test_improvement_next_step_bridge_script.py`
- `tests/test_improvement_next_step_view_script.py`
- `tests/test_improvement_view_script.py`
- `tests/test_auto_continue_decision_input_script.py`
- `tests/test_mainline_monitoring_script.py`
- `tests/test_official_fetch_scripts.py`
- `tests/test_main.py`
- `tests/test_system.py`
- `tests/test_checkpoint001_emit_script.py`

#### スクリプト
- `scripts/build_real_data_csv.py`
- `scripts/checkpoint001_emit_contract.py`
- `scripts/fetch_fred_series.py`
- `scripts/fetch_treasury_series.py`
- `scripts/refresh_mainline_monitoring.py`
- `scripts/run_monitoring_orchestrator.py`
- `scripts/run_single_candidate_orchestrator.py`
- `scripts/view_auto_continue_decision_input.py`
- `scripts/view_improvement_auto_continue.py`
- `scripts/view_improvement_auto_continue_summary.py`
- `scripts/view_improvement_handoff.py`
- `scripts/view_improvement_next_step.py`
- `scripts/view_improvement_next_step_bridge.py`
- `scripts/view_improvement_records.py`

#### 設定・データ・出力
- `configs/` — 全 JSON ファイル
- `data/` — 全データファイル
- `outputs/` — 全出力ファイル

#### ドキュメント
- `docs/strategy_comparison_summary.md`
- `docs/checkpoint_002_issue.md`
- `docs/checkpoint1_restart_scope.md`
- `docs/checkpoint_status.md`
- `docs/checkpoint_pr_template.md`
- `docs/checkpoint_machine_check_items.md`
- `docs/draft_issue_bounded_tiingo_pacing.md`
- `docs/draft_issue_editorconfig.md`
- `docs/multi_ai_monitoring_orchestration.md`
- `docs/multi_ai_single_candidate_orchestration.md`

#### その他
- `package.json`

### foundation に残すもの

#### 統治・テンプレート
- `CLAUDE.md` — agentgov 運用ルール
- `AGENTS.md` → `.template/AGENTS.md` に差し替え
- `PLAN.md` → `.template/PLAN.md` に差し替え
- `SPEC.md` → `.template/SPEC.md` に差し替え
- `README.md` → `.template/README.md` に差し替え

#### GitHub
- `.github/ISSUE_TEMPLATE/checkpoint.md`
- `.github/pull_request_template.md`
- `.github/workflows/ci.yml`（pre-test-script を削除）
- `.github/workflows/pr-invariants.yml`

#### スクリプト（統治系）
- `scripts/check_pr_invariants.py`

#### テスト（統治系）
- `tests/test_check_pr_invariants.py`

#### ドキュメント（統治系）
- `docs/checkpoint_state_machine.md`
- `docs/claude_checkpoint_workflow.md`
- `docs/ai_role_split.md`
- `docs/foundation_boundary.md`
- `docs/foundation_repo_extraction_plan.md`
- `docs/template_usage_guide.md`
- `docs/app_migration_plan.md`（本ドキュメント）

#### 開発環境
- `pyproject.toml`（name を変更、dependencies は空のまま）
- `.pre-commit-config.yaml`
- `.editorconfig`
- `.gitignore`
- `.gitattributes`
- `.mcp.json`（パスをプレースホルダーに）
- `uv.lock`

#### テンプレートファイル
- `.template/README.md`
- `.template/AGENTS.md`
- `.template/PLAN.md`
- `.template/SPEC.md`

---

## app-investment repo の構成

```
app-investment/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── checkpoint.md
│   ├── pull_request_template.md
│   └── workflows/
│       ├── ci.yml
│       └── pr-invariants.yml
├── src/
│   ├── main.py
│   └── investment_system/
│       ├── __init__.py
│       ├── backtest.py
│       ├── cli.py
│       ├── compare.py
│       ├── config.py
│       ├── data_loader.py
│       ├── ... (全モジュール)
│       └── orchestrator/
├── tests/
│   └── (全ドメインテスト)
├── scripts/
│   └── (全ドメインスクリプト)
├── configs/
├── data/
├── outputs/
├── docs/
├── CLAUDE.md
├── AGENTS.md       ← 現行版をそのまま使用
├── PLAN.md         ← §1 以降の投資ロジック部分
├── SPEC.md         ← 現行版をそのまま使用
├── README.md       ← 現行版をそのまま使用
├── pyproject.toml  ← name="app-investment"
├── .pre-commit-config.yaml
├── .editorconfig
├── .gitignore
├── .gitattributes
└── uv.lock
```

---

## 移行手順

### Phase A: app-investment repo 作成

#### Step 1: GitHub に空 repo を作成
```bash
gh repo create townkaminoma-sketch/app-investment --private --description "Investment system — built on foundation-template"
```

#### Step 2: foundation-template をベースにクローン
```bash
gh repo clone townkaminoma-sketch/python-template app-investment
cd app-investment
git remote set-url origin https://github.com/townkaminoma-sketch/app-investment.git
```

注意: git history を引き継ぐ。foundation と共有する歴史を維持する。

#### Step 3: 不要な foundation-only ファイルを削除
- `.template/` ディレクトリを削除
- `docs/foundation_boundary.md` を削除
- `docs/foundation_repo_extraction_plan.md` を削除
- `docs/template_usage_guide.md` を削除
- `docs/app_migration_plan.md` を削除

#### Step 4: ドキュメントを投資固有版に整理
- `PLAN.md` から §0（Foundation ロードマップ）を削除、§1 以降を残す
- `AGENTS.md`, `SPEC.md`, `README.md` はそのまま（既に投資固有）

#### Step 5: pyproject.toml を調整
```toml
[project]
name = "app-investment"
version = "0.1.0"
description = "Investment system — built on foundation-template"
```

#### Step 6: CI を調整
- `ci.yml`: pre-test-script はそのまま（Tiingo CSV 生成）
- secrets: `TIINGO_API_TOKEN` を app-investment repo にも設定

#### Step 7: テスト実行
```bash
python -m uv sync --dev
python -m uv run pytest
python -m uv run ruff check .
```

#### Step 8: 初回 push
```bash
git add -A
git commit -m "feat: initialize app-investment from foundation-template"
git push origin main
```

### Phase B: foundation-template クリーンアップ

#### Step 1: app 固有ファイルを削除
```bash
# ソースコード
rm -rf src/investment_system/
rm src/main.py

# テスト（foundation テスト以外）
rm tests/test_checkpoint1_*.py
rm tests/test_checkpoint2_*.py
rm tests/test_checkpoint3_*.py
rm tests/test_cli_checkpoint1_horizons.py
rm tests/test_orchestration.py
rm tests/test_improvement_*.py
rm tests/test_auto_continue_*.py
rm tests/test_mainline_monitoring_script.py
rm tests/test_official_fetch_scripts.py
rm tests/test_main.py
rm tests/test_system.py
rm tests/test_checkpoint001_emit_script.py

# スクリプト（統治系以外）
rm scripts/build_real_data_csv.py
rm scripts/checkpoint001_emit_contract.py
rm scripts/fetch_fred_series.py
rm scripts/fetch_treasury_series.py
rm scripts/refresh_mainline_monitoring.py
rm scripts/run_monitoring_orchestrator.py
rm scripts/run_single_candidate_orchestrator.py
rm scripts/view_*.py

# 設定・データ・出力
rm -rf configs/
rm -rf data/
rm -rf outputs/

# ドメイン固有ドキュメント
rm docs/strategy_comparison_summary.md
rm docs/checkpoint_002_issue.md
rm docs/checkpoint1_restart_scope.md
rm docs/checkpoint_status.md
rm docs/checkpoint_pr_template.md
rm docs/checkpoint_machine_check_items.md
rm docs/draft_issue_bounded_tiingo_pacing.md
rm docs/draft_issue_editorconfig.md
rm docs/multi_ai_monitoring_orchestration.md
rm docs/multi_ai_single_candidate_orchestration.md

# その他
rm package.json
```

#### Step 2: .template/ をルートに昇格
```bash
cp .template/README.md README.md
cp .template/AGENTS.md AGENTS.md
cp .template/PLAN.md PLAN.md
cp .template/SPEC.md SPEC.md
rm -rf .template/
```

#### Step 3: pyproject.toml を調整
```toml
[project]
name = "foundation-template"
version = "1.0.0"
description = "Checkpoint-gated AI-assisted development template"
```

#### Step 4: ci.yml から pre-test-script を削除
pre-test-script が不要になるため、with: から削除。

#### Step 5: .mcp.json をプレースホルダーに
```json
{
  "mcpServers": {
    "agentgov": {
      "command": "uv",
      "args": ["run", "python", "<path-to-agentgov>/server.py"],
      "role": "orchestrator"
    }
  }
}
```

#### Step 6: テスト実行
```bash
python -m uv run pytest    # test_check_pr_invariants のみ pass
python -m uv run ruff check .
```

#### Step 7: GitHub template repository 設定
Settings → General → Template repository にチェック

#### Step 8: コミット・push
```bash
git add -A
git commit -m "feat: complete foundation-template by removing app-specific code"
git push origin main
```

---

## Rollback 計画

| 段階 | 問題 | 対応 |
|------|------|------|
| Phase A Step 7 | app-investment でテスト失敗 | import パス不整合を修正。最悪 repo を削除して再試行 |
| Phase B Step 1 | 削除すべきでないファイルを消した | `git revert` で即座に復元 |
| Phase B Step 6 | foundation のテストが壊れた | `git revert` で app 固有ファイルが戻り、元の状態に復帰 |
| 全体 | 分離自体を撤回したい | app-investment repo を削除、foundation の revert で完全復元 |

**重要**: Phase A と Phase B は独立。Phase A が成功してから Phase B に進む。Phase B で問題があっても Phase A には影響しない。

---

## 検証チェックリスト

### app-investment
- [ ] `pytest` で全テスト pass（現行 219 テスト）
- [ ] `ruff check .` clean
- [ ] CI green（shared-workflows 経由）
- [ ] pr-invariants が動作する
- [ ] `python -m src.main report --config configs/default.json` が実行可能
- [ ] `python -m src.main backtest --config configs/default.json` が実行可能

### foundation-template
- [ ] `pytest` pass（`test_check_pr_invariants` のみ）
- [ ] `ruff check .` clean
- [ ] CI green
- [ ] "Use this template" で新規 repo 作成可能
- [ ] 新規 repo で CI green
- [ ] app 固有のファイルが残っていない
- [ ] `.template/` が削除されている（ルートに昇格済み）

---

## タイムライン

| Phase | 内容 | 想定時間 |
|-------|------|----------|
| Phase A | app-investment 作成・テスト | 1 checkpoint |
| Phase B | foundation クリーンアップ | 1 checkpoint |
| 検証 | 両 repo の CI green 確認 | Phase B に含む |

Phase A = Foundation CP5、Phase B = Foundation CP5 の後半または CP6
