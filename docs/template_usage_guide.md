# Foundation Template 利用ガイド

## 概要

`python-template` は checkpoint 方式で AI 協調開発を行うための foundation-template です。
新しいプロジェクトを始めるときは、この template を起点にします。

## 前提

- GitHub アカウントがあること
- Python 3.11 以上がインストールされていること
- uv がインストール可能であること
- Git が使えること

## 新規プロジェクトの作り方

### Step 1: GitHub で新規リポジトリを作成

1. [python-template](https://github.com/townkaminoma-sketch/python-template) を開く
2. "Use this template" → "Create a new repository" を選択
3. リポジトリ名と visibility を設定して作成

### Step 2: clone とセットアップ

```bash
git clone https://github.com/townkaminoma-sketch/<repo-name>.git
cd <repo-name>
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install uv
python -m uv sync --dev
python -m pre_commit install
```

### Step 3: テンプレートファイルの初期化

`.template/` ディレクトリに foundation 用の初期ファイルがあります。
必要に応じてルートにコピーして、プロジェクトに合わせて編集してください。

```bash
cp .template/README.md README.md
cp .template/AGENTS.md AGENTS.md
cp .template/PLAN.md PLAN.md
cp .template/SPEC.md SPEC.md
```

各ファイルの `<!-- -->` コメント部分をプロジェクト固有の内容に書き換えてください。

### Step 4: pyproject.toml の調整

`pyproject.toml` の以下を書き換えてください:

- `name` — プロジェクト名
- `version` — 初期バージョン
- `description` — プロジェクトの説明
- `dependencies` — プロジェクト固有の依存パッケージ

### Step 5: 動作確認

```bash
python -m uv run pytest
python -m uv run ruff check .
```

### Step 6: 最初の checkpoint を始める

1. `PLAN.md` に最初の checkpoint を記載する
2. GitHub Issue を checkpoint テンプレートで作成する
3. ブランチを切って実装する
4. PR を作成し、CI green を確認する
5. 人間が承認して merge する

## テンプレートに含まれるもの

### 統治・運用

| ファイル | 役割 |
|----------|------|
| `CLAUDE.md` | agentgov 運用ルール |
| `.github/ISSUE_TEMPLATE/checkpoint.md` | checkpoint Issue テンプレート |
| `.github/pull_request_template.md` | PR テンプレート |
| `scripts/check_pr_invariants.py` | PR scope チェック |

### CI

| ファイル | 役割 |
|----------|------|
| `.github/workflows/ci.yml` | Python CI（shared-workflows 経由） |
| `.github/workflows/pr-invariants.yml` | PR invariant チェック（shared-workflows 経由） |

### 開発環境

| ファイル | 役割 |
|----------|------|
| `pyproject.toml` | プロジェクト設定（dev deps: pytest, ruff, pre-commit） |
| `.pre-commit-config.yaml` | pre-commit hooks |
| `.editorconfig` | エディタ書式設定 |
| `.gitignore` | Git 除外設定 |
| `.gitattributes` | 改行コード設定 |

### ドキュメント

| ファイル | 役割 |
|----------|------|
| `docs/checkpoint_state_machine.md` | checkpoint 状態遷移の定義 |
| `docs/claude_checkpoint_workflow.md` | checkpoint 運用手順 |
| `docs/ai_role_split.md` | AI 役割分担 |
| `docs/foundation_boundary.md` | foundation / app 境界定義 |
| `docs/template_usage_guide.md` | 本ドキュメント |

## checkpoint 運用の流れ

1. Issue を checkpoint テンプレートで作成
2. ブランチを切る（`checkpoint-<name>` 等）
3. 最小差分で実装
4. PR を作成（PR テンプレートの全項目を埋める）
5. CI green を確認
6. 人間が承認して merge
7. 次の checkpoint へ

詳しくは `docs/checkpoint_state_machine.md` を参照してください。

## agentgov を使う場合

`CLAUDE.md` に agentgov の運用ルールが定義されています。
`.mcp.json` の接続先パスをローカル環境に合わせて調整してください。

## 注意事項

- `.template/` 内のファイルはルートにコピーしてから使ってください
- `pyproject.toml` の project name / version は必ず書き換えてください
- `.mcp.json` のパスは環境に合わせて調整してください
- CI は `townkaminoma-sketch/shared-workflows` を参照しています
