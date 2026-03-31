---
name: Checkpoint
about: Create one checkpoint issue
title: "[CP] "
labels: ["checkpoint"]
assignees: []
---

## Background
なぜ今この checkpoint が必要か

## Purpose
この checkpoint で達成したいこと

## Non-goals
この checkpoint ではやらないこと

## Scope
変更してよい範囲
（`docs-only` / `workflow-only` / `config-only` など純度が重要なら、ここかタイトルで明示）

## Out of scope
変更してはいけない範囲
（侵食しやすいパス・領域は具体的に列挙）

## Done conditions
完了とみなす条件
- [ ] Out of scope に書いた領域への変更がない
- [ ] Expected files の想定から大きく外れていない（外れる場合は本 Issue を更新した）

## Rollback conditions
rollback 候補とみなす条件
- [ ] 対象外の変更が混ざっておらず、revert など 1 手で戻せる見込みである

## Expected files
変更が想定されるファイル
（レビュー時は実 diff と突き合わせる想定変更範囲）

## Test plan
実行予定のテスト
（実行しなかったものは「未実行」と書き、完了扱いにしない）

## Risks
想定リスク

## Notes for AI
- 1 checkpoint だけ
- 最小差分
- 無関係変更禁止
- テスト未実行なら完了扱い禁止
