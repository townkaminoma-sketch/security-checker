# [プロジェクト名]

<!-- このファイルは foundation-template から生成されました。プロジェクトに合わせて書き換えてください。 -->

## 概要

このプロジェクトの目的を1-2文で記載してください。

## セットアップ

1. GitHub で [foundation-template](https://github.com/townkaminoma-sketch/python-template) から "Use this template" で新規リポジトリを作成
2. clone する
   ```
   git clone https://github.com/townkaminoma-sketch/<repo-name>.git
   cd <repo-name>
   ```
3. 仮想環境を作る
   ```
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. uv を入れる
   ```
   python -m pip install uv
   ```
5. 依存関係を同期する
   ```
   python -m uv sync --dev
   ```
6. pre-commit を有効化する
   ```
   python -m pre_commit install
   ```
7. 動作確認
   ```
   python -m uv run pytest
   python -m uv run ruff check .
   ```

## 開発の進め方

このプロジェクトは checkpoint 方式で開発を進めます。

- 1 Issue = 1 checkpoint
- 1 PR = 1 目的
- 最小差分で変更する
- CI が緑でない限り merge しない
- 最終承認は人間が行う

詳しくは以下を参照してください:
- `CLAUDE.md` — agentgov 運用ルール
- `AGENTS.md` — 開発環境・確認ルール
- `PLAN.md` — checkpoint 計画
- `SPEC.md` — 仕様定義
- `docs/checkpoint_state_machine.md` — 状態遷移の定義

## テスト

```
python -m uv run pytest
```

## Lint

```
python -m uv run ruff check .
```

## CI

push と pull request で GitHub Actions の CI が走ります。
CI は [shared-workflows](https://github.com/townkaminoma-sketch/shared-workflows) の reusable workflow を使用しています。

## ファイル構成

```
src/              — アプリケーションコード
tests/            — テスト
scripts/          — ユーティリティスクリプト
docs/             — ドキュメント
.github/          — CI / Issue / PR テンプレート
CLAUDE.md         — agentgov 運用ルール
AGENTS.md         — 開発環境・確認ルール
PLAN.md           — checkpoint 計画
SPEC.md           — 仕様定義
pyproject.toml    — プロジェクト設定
```
