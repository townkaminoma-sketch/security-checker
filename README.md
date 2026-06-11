# repo-security-checker

`repo-security-checker` は、複数のセキュリティスキャナを束ねて 1 本の JSON レポート（`SecurityReport`）に集約する Python CLI です。CI に組み込み、`high` / `critical` の検出があれば exit code 1 を返してパイプラインをブロックする「セキュリティゲート」として動作します。

## 同梱するスキャナ

| スキャナ | 対象 | 役割 |
|---|---|---|
| [gitleaks](https://github.com/gitleaks/gitleaks) | リポジトリ全体 | シークレット漏洩検査 |
| [pip-audit](https://github.com/pypa/pip-audit) | Python 依存パッケージ | 既知脆弱性（CVE）検査 |
| [bandit](https://github.com/PyCQA/bandit) | Python ソースコード | 静的解析（SAST） |

各スキャナの結果は正規化されて 1 本の JSON にマージされます。

## 使い方

```bash
repo-security-checker scan --target-dir src --output security-report.json
```

主なオプション:

- `--target-dir <dir>` — スキャン対象ディレクトリ（デフォルト: `.`）
- `--output <path>` — レポート出力先 JSON パス（デフォルト: `security-report.json`）
- `--min-severity <level>` — 指定した重大度以上の finding だけをレポートに残す（`low` / `medium` / `high` / `critical`。デフォルト: 未指定 = 全件保持）

### --min-severity による絞り込み

ノイズの多いリポジトリで重要な検出だけに注目したい場合に使います。

```bash
repo-security-checker scan --target-dir src --min-severity high
```

- 指定した重大度より低い finding はレポート出力から除外されます
- フィルタは終了コード判定の前に適用されます。除外された finding は exit code にも影響しません

終了コード:

- `0` — 検出なし、または `low` / `medium` / `info` のみ
- `1` — `high` または `critical` を 1 件以上検出（CI ゲートとして機能）

出力 JSON は `findings[]` を含む `SecurityReport` 構造で、各 finding に tool / severity / title / detail / file / line が入ります。

## CI 連携

`.github/workflows/security-scan.yml` が [shared-workflows](https://github.com/townkaminoma-sketch/shared-workflows) の reusable workflow を呼び出し、main への push と pull request で `repo-security-checker scan` を実行します。`high` / `critical` 検出時はジョブが失敗し、PR をブロックします。

## セットアップ

Python 3.11、依存管理は [uv](https://github.com/astral-sh/uv) を使用します。

```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install uv
python -m uv sync --dev
python -m pre_commit install
```

## 開発コマンド

```bash
# テスト
python -m uv run pytest

# Lint
python -m uv run ruff check .
```

## ファイル構成

```
src/repo_security_checker/   — CLI 本体・スキャナアダプタ・レポート集約
tests/                       — pytest テスト
.github/workflows/           — CI（security-scan, shared-workflows 連携）
docs/                        — 仕様補助ドキュメント
CLAUDE.md                    — agentgov 運用ルール（本リポ）
AGENTS.md                    — 開発環境・確認ルール
SPEC.md                      — 仕様定義
PLAN.md                      — checkpoint 計画
docs/checkpoint_state_machine.md — checkpoint 状態遷移
pyproject.toml               — プロジェクト設定
```

## 関連ドキュメント

- `CLAUDE.md` — agentgov によるタスク管理・ロール・自動化レベル
- `AGENTS.md` — 開発環境のルール
- `SPEC.md` — `SecurityReport` スキーマ・スキャナ仕様
- `PLAN.md` — checkpoint 計画
- `docs/checkpoint_state_machine.md` — 状態遷移の定義
