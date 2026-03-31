# agentgov 運用ルール

本リポジトリは agentgov（MCP サーバー）でタスク管理する。

## 目的

このリポジトリでは、AI の役割を分離し、
最小差分・明確な承認・監査可能な状態遷移で開発を進める。

基本原則は以下とする。

- 1 Issue = 1目的
- 1 PR = 1最小差分
- scope 外変更は禁止
- CI / Test を必須ゲートとする
- 人間承認なしで done にしない
- rejected 時は理由を残す
- 曖昧な作業は Level 1 に下げる

## ロール

### orchestrator
担当: Claude Code

役割:
- 目的固定
- task 登録
- レビュー
- 評価
- 承認判断の補助
- CI 実行と結果確認
- 次アクション整理

禁止:
- 実コード変更をしない
- 実装を直接進めない
- human approval なしで done にしない

### executor
担当: Cursor

役割:
- 許可された範囲だけ実装する
- 最小差分で修正する
- 実装結果を記録する
- 指定されたテストを実行する

禁止:
- scope を広げない
- 承認しない
- done にしない
- task 内容を勝手に変更しない

## agentgov の現行 task schema

agentgov の `write_task` で現状登録できる項目は以下のみとする。

- `title`
- `description`
- `acceptance_criteria`
- `required_artifacts`
- `owner_role`
- `risk_level`

`write_task` には schema に存在しない項目を直接追加しない。

## schema 外の運用項目

以下の項目は運用上は重要だが、現行の agentgov contract schema には未実装である。

- objective
- scope
- allowed_files
- change_budget
- automation_level
- rollback_plan
- reason_code

これらは `description`、Issue、task.md、PR 説明などに明示する。

## description の書き方

`description` には、必要に応じて以下を構造化して含める。

- Objective
- Scope
- Allowed files
- Change budget
- Rollback plan
- Notes

例:

```text
Objective:
設定骨組みの追加を行う

Scope:
設定ロードの最小骨組みのみ。通知処理は含まない

Allowed files:
- src/example/config.py
- tests/test_config.py

Change budget:
最小差分。新規ファイル追加と必要最小限のテストのみ

Rollback plan:
追加ファイルを戻せば元に戻る状態を維持する
```

## 基本フロー

1. orchestrator が write_task で task 登録
2. orchestrator が update_status(pending) にする
3. executor が update_status(in_progress) にする
4. executor が実装する
5. executor が write_result で結果を記録する
6. executor が update_status(evaluation) にする
7. orchestrator が evaluate_result を実行する
8. orchestrator が必要に応じて trigger_ci を実行する
9. orchestrator が report_ci で結果確認する
10. human approval を確認する
11. orchestrator が update_status(approved) にする
12. orchestrator が update_status(done) にする

## モード B: orchestrator 直接実装（シングルエージェント）

Cursor を使わず Claude Code だけで進める場合:

1. orchestrator が write_task → update_status(pending) まで進める
2. Agent ツール（subagent）に実装を委任する
3. subagent が update_status(in_progress) → 実装 → write_result → update_status(evaluation) まで進める
4. orchestrator が evaluate_result 以降を実行する

重要: orchestrator が直接実装しない。必ず subagent に委任する。orchestrator ロールでは write_result が呼べず、in_progress にも遷移できないため。

## rejected 時の流れ

1. orchestrator が差し戻し理由を整理する
2. reason_code を記録する
3. orchestrator が update_status(pending) に戻す
4. executor が再開して修正する
5. 再度 evaluation に進める

## 自動化レベル

| Level   | 適用場面                     | risk_level | 運用                   |
|---------|------------------------------|------------|------------------------|
| Level 1 | 新規設計・基盤変更・仕様曖昧 | high       | 人間確認を厚くする     |
| Level 2 | 既存パターンの拡張           | medium     | 通常運用               |
| Level 3 | typo・文言修正・軽微リネーム | low        | 定型処理として委任可能 |

## 実装ルール

- 最小差分で変更する
- 許可されていないファイルは触らない
- 不要なリファクタをしない
- 関係ない rename をしない
- ついで修正をしない
- acceptance criteria を満たすことを優先する

## 評価ルール

評価では以下を確認する。

- task の目的に沿っているか
- scope 外変更がないか
- 差分が最小か
- テストが通っているか
- required_artifacts が揃っているか
- rollback 可能か
- 監査ログが残っているか

## human approval 必須条件

以下は human approval 必須とする。

- Level 1 の全変更
- public interface 変更
- config / policy / CI / deploy 変更
- データ形式変更
- 破壊的変更
- 判定基準変更

## reason_code の例

- INITIAL_SETUP
- SCOPE_VIOLATION
- TEST_FAILURE
- CI_FAILURE
- REVIEW_REJECTED
- MISSING_EVIDENCE
- CHANGE_BUDGET_EXCEEDED

## 運用メモ

- 迷ったら自動化レベルを下げる。
- 迷ったら pending に戻す。
- 迷ったら人間に確認する。

## agentgov 運用ルール

本リポジトリは agentgov（MCP サーバー）でタスク管理する。

### 基本フロー

1. `write_task` で contract 登録 → `update_status(pending)`
2. executor が `update_status(in_progress)` → 実装 → `write_result` → `update_status(evaluation)`
3. orchestrator が `evaluate_result` → `trigger_ci` → `report_ci`
4. `update_status(approved)` → `update_status(done)`

### ロール

- **orchestrator** (Claude Code): 設計・レビュー・承認。実コード変更しない
- **executor** (Cursor): 実装のみ。承認できない

### 自動化レベル

| Level | 適用場面 | risk_level |
|---|---|---|
| Level 1 (慎重) | 新規設計・基盤変更 | high |
| Level 2 (通常) | 既存パターンの拡張 | medium |
| Level 3 (委任) | typo・ドキュメント・リネーム | low |

### rejected 時

orchestrator が `update_status(pending)` → executor が再開 → 修正 → 再評価

## 事前包括許可（preapproved actions）

以下をすべて満たす場合、executor は追加確認なしで進めてよい。

### 条件

- repo 内の変更である
- Allowed files 内のみを変更する
- public interface を変更しない
- config schema を変更しない
- CI / policy / deploy / hooks を変更しない
- rename / move / delete をしない
- 新規依存を追加しない
- Change budget 内に収まる
- acceptance criteria 達成に必要な最小差分である

### 確認なしで実行してよい作業

- Allowed files 内の実装
- 必要最小限のテスト追加・修正
- import 整理
- docstring / コメント修正
- 指定された lint / test の実行
- 実装に伴う軽微な定数・型・エラーメッセージ調整

### 次の場合のみ人間確認

- Allowed files 外に触れる必要がある
- public interface 変更が必要
- config schema 変更が必要
- 新規依存追加が必要
- Change budget を超える
- acceptance criteria を満たせない
- 破壊的変更が必要
