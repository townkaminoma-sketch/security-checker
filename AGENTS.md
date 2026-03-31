# AGENTS.md

## セットアップ手順

1. `py -m venv .venv`
2. `.\.venv\Scripts\Activate.ps1`
3. `python -m pip install uv`
4. `python -m uv sync --dev`
5. `python -m pre_commit install`

## テスト手順

`python -m uv run pytest`

## lint 手順

`python -m uv run ruff check .`

## pre-commit 手順

- フック有効化: `python -m pre_commit install`
- 手動実行: `python -m pre_commit run --all-files`

## 変更時の確認ルール

- Python コードや設定を変更したら `python -m uv run pytest` を実行する
- Python コードや設定を変更したら `python -m uv run ruff check .` を実行する
- コミット前に `python -m pre_commit run --all-files` を実行する

## 開発運用の原則

- 既存の土台を壊さず、最小差分で追加する
- 目的に関係ないファイルは触らない
- 未実行は未実行と明記する
- `pytest`、`ruff check .`、`pre-commit run --all-files` を通したものだけ完了扱いにする
- 現在の実行環境では `cmd` / Python / Bash を優先し、PowerShell は必要時のみ使う
