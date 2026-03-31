# Foundation Boundary Definition

本ドキュメントは `python-template` を foundation-template に育てるにあたり、
**foundation 層に残すもの** と **app 層に移すもの** の境界を確定する。

## 判断基準

| 条件 | 判断 |
|------|------|
| どの app でも必要な統治ルール | foundation に残す |
| どの app でも必要な開発環境設定 | foundation に残す |
| checkpoint 運用に必要な仕組み | foundation に残す |
| 特定ドメインの知識が必要 | app に移す |
| 特定 API やデータソースに依存 | app に移す |
| ドメイン固有のロジック・データ・出力 | app に移す |

---

## Foundation に残すもの

### 統治・運用ドキュメント

| ファイル | 理由 |
|----------|------|
| `CLAUDE.md` | agentgov 運用ルール（全 app 共通） |
| `AGENTS.md` | 開発環境・確認ルール（テンプレートとして） |
| `PLAN.md` | checkpoint 計画テンプレート（内容は app ごとに書き換え） |
| `README.md` | テンプレート利用ガイド（内容は書き換え） |
| `SPEC.md` | 仕様テンプレート（内容は書き換え） |

### GitHub テンプレート・CI

| ファイル | 理由 |
|----------|------|
| `.github/ISSUE_TEMPLATE/checkpoint.md` | checkpoint Issue の定型フォーマット |
| `.github/pull_request_template.md` | PR の必須記載項目 |
| `.github/workflows/ci.yml` | CI テンプレート（後に shared-workflows へ移行） |
| `.github/workflows/pr-invariants.yml` | PR scope チェック |

### 開発環境設定

| ファイル | 理由 |
|----------|------|
| `pyproject.toml` | 最小構成（dev deps のみ: pytest, ruff, pre-commit） |
| `.pre-commit-config.yaml` | pre-commit hooks 設定 |
| `.editorconfig` | エディタ書式統一 |
| `.gitignore` | 共通除外パターン |
| `.gitattributes` | 改行コード統一 |
| `uv.lock` | 依存関係ロック |

### agentgov 連携

| ファイル | 理由 |
|----------|------|
| `.mcp.json` | agentgov 接続設定（パスは app ごとに調整） |

### スクリプト（統治系のみ）

| ファイル | 理由 |
|----------|------|
| `scripts/check_pr_invariants.py` | PR scope チェックロジック |

### checkpoint 運用ドキュメント

| ファイル | 理由 |
|----------|------|
| `docs/checkpoint_state_machine.md` | 状態遷移の定義（全 app 共通） |
| `docs/claude_checkpoint_workflow.md` | checkpoint 運用手順（全 app 共通） |
| `docs/ai_role_split.md` | AI 役割分担（全 app 共通） |
| `docs/foundation_boundary.md` | 本ドキュメント（境界定義） |
| `docs/foundation_repo_extraction_plan.md` | 分離計画 |

### ディレクトリ骨格

| ディレクトリ | 理由 |
|--------------|------|
| `src/` | app がここにコードを置く（空で保持） |
| `tests/` | app がここにテストを置く（空で保持） |
| `scripts/` | 統治系スクリプトのみ残す |

---

## App に移すもの

### ドメインロジック（src/investment_system/）

| ファイル | 理由 |
|----------|------|
| `src/investment_system/__init__.py` | ドメイン固有パッケージ |
| `src/investment_system/backtest.py` | 投資バックテストロジック |
| `src/investment_system/signals.py` | 投資シグナル評価 |
| `src/investment_system/portfolio.py` | ポートフォリオ構築 |
| `src/investment_system/risk.py` | リスク評価 |
| `src/investment_system/compare.py` | 戦略比較 |
| `src/investment_system/report.py` | レポート生成 |
| `src/investment_system/config.py` | ドメイン固有設定ローダー |
| `src/investment_system/data_loader.py` | データ読み込み |
| `src/investment_system/cli.py` | ドメイン固有 CLI |
| `src/investment_system/orchestration.py` | マルチAIオーケストレーション |
| `src/investment_system/shared_foundation.py` | 投資ロジック共通基盤 |
| `src/investment_system/horizon_skeletons.py` | horizon 骨格 |
| `src/investment_system/checkpoint1_*.py` | 投資 checkpoint 1 関連 |
| `src/investment_system/checkpoint2_runner.py` | 投資 checkpoint 2 関連 |
| `src/investment_system/checkpoint3_compare.py` | 投資 checkpoint 3 関連 |
| `src/investment_system/orchestrator/` | orchestrator サブパッケージ |
| `src/main.py` | ドメイン固有エントリポイント |

### ドメイン固有設定

| ファイル | 理由 |
|----------|------|
| `configs/*.json`（全ファイル） | 投資戦略パラメータ |

### ドメイン固有データ・出力

| ディレクトリ | 理由 |
|--------------|------|
| `data/` | 投資データ |
| `outputs/` | バックテスト出力 |

### ドメイン固有スクリプト

| ファイル | 理由 |
|----------|------|
| `scripts/build_real_data_csv.py` | Tiingo データ取得 |
| `scripts/checkpoint001_emit_contract.py` | 投資 checkpoint 契約出力 |
| `scripts/fetch_fred_series.py` | FRED データ取得 |
| `scripts/fetch_treasury_series.py` | 財務データ取得 |
| `scripts/refresh_mainline_monitoring.py` | 監視更新 |
| `scripts/run_monitoring_orchestrator.py` | 監視オーケストレーター |
| `scripts/run_single_candidate_orchestrator.py` | 候補オーケストレーター |
| `scripts/view_*.py`（全ファイル） | ドメイン固有ビューア |

### ドメイン固有テスト

| ファイル | 理由 |
|----------|------|
| `tests/test_checkpoint1_*.py` | 投資 checkpoint テスト |
| `tests/test_checkpoint2_*.py` | 投資 checkpoint テスト |
| `tests/test_checkpoint3_*.py` | 投資 checkpoint テスト |
| `tests/test_orchestration.py` | オーケストレーションテスト |
| `tests/test_improvement_*.py` | 改善系テスト |
| `tests/test_auto_continue_*.py` | 自動継続テスト |
| `tests/test_mainline_monitoring_script.py` | 監視テスト |
| `tests/test_official_fetch_scripts.py` | データ取得テスト |
| `tests/test_main.py` | ドメインエントリポイントテスト |
| `tests/test_system.py` | システムテスト |
| `tests/test_cli_checkpoint1_horizons.py` | CLI テスト |
| `tests/test_checkpoint001_emit_script.py` | 契約出力テスト |

### ドメイン固有ドキュメント

| ファイル | 理由 |
|----------|------|
| `docs/strategy_comparison_summary.md` | 戦略比較結果 |
| `docs/checkpoint_002_issue.md` | 投資 checkpoint 2 Issue 下書き |
| `docs/checkpoint1_restart_scope.md` | 投資 checkpoint 1 scope |
| `docs/checkpoint_status.md` | 投資 checkpoint 進捗 |
| `docs/checkpoint_pr_template.md` | 投資固有 PR テンプレ下書き |
| `docs/checkpoint_machine_check_items.md` | 投資固有チェック項目 |
| `docs/draft_issue_bounded_tiingo_pacing.md` | Tiingo Issue 下書き |
| `docs/draft_issue_editorconfig.md` | editorconfig Issue 下書き |
| `docs/multi_ai_monitoring_orchestration.md` | マルチAI監視 |
| `docs/multi_ai_single_candidate_orchestration.md` | マルチAI候補 |

### その他

| ファイル | 理由 |
|----------|------|
| `package.json` | 用途不明（投資 app 固有と判断） |

---

## Foundation テンプレート適用時の手順（将来）

新しい app repo を作るとき:

1. foundation-template を GitHub template として Use this template
2. `src/` に自分の app パッケージを作成
3. `tests/` にテストを作成
4. `PLAN.md` を自分の checkpoint 計画に書き換え
5. `AGENTS.md` を自分の環境に合わせて調整
6. `pyproject.toml` にドメイン固有の依存を追加
7. CI が green であることを確認

---

## 注意事項

- この境界定義は **現時点の判断** であり、app 分離時に微調整する可能性がある
- `scripts/check_pr_invariants.py` のテスト（`tests/test_check_pr_invariants.py`）は foundation 側に残す
- `.mcp.json` のパスは app ごとに異なるため、テンプレートではプレースホルダーにする
- `pyproject.toml` の project name / version は app ごとに書き換え前提
