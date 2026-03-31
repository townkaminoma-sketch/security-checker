# CLAUDE.md 前提の checkpoint 運用フロー

`CLAUDE.md` は入口メモであり、**本書は「誰が・どの順で・何を確認して checkpoint を進めるか」** を固定する。
実装挙動は変えない（運用の型だけ）。

## 役割の前提（再掲）

| 役割 | 主な担当 | 参照 |
|------|-----------|------|
| Claude Code | 読解、`gh` で Issue/PR 確認、小さな実装計画・リスク・レビュー観点 | `docs/ai_role_split.md` |
| Cursor / Codex | 承認済みの **最小差分** の実装・テスト・コミット・PR | `AGENTS.md` |
| 人間 | merge / hold、優先度、スコープの最終判断 | Issue / PR |

## 操作手順（標準）

1. **Issue を 1 本選ぶ**（1 Issue = 1 checkpoint）。スコープ・非スコープ・Expected files を埋める（テンプレ参照）。
2. **ブランチを切る**（`main` 起点、名前は checkpoint 専用）。
3. **変更は最小差分**（無関係ファイルに触れない）。
4. **ローカル検証**（`AGENTS.md`）:
   - `python -m uv run pytest`
   - `python -m uv run ruff check .`
   - `python -m uv run pre-commit run --all-files`（または変更ファイルに限定）
5. **PR を開く** — Purpose / Non-goals / 変更ファイル / テスト結果 / 未実行の明示。
6. **CI が緑になるまで merge しない**。
7. **Squash merge 等**はリポジトリ運用に従う。

PR ブランチに **最新 `main` を取り込む**ときは `git merge origin/main`（または `rebase`）でよい。コンフリクトは **`main` 側の意図を保ちつつ** PR の差分を統合する。取り込み後は `pytest` / `ruff` / `pre-commit` を再実行し（マージ直後は `git diff` が空になり得るので **`pre-commit run --all-files` 併用**）、`git push` してから PR を更新する。

### main への統合（安全）

`main` へ反映するときは **GitHub の PR マージ**（UI）または **`gh pr merge`** のみとする（Squash / Merge commit / Rebase and merge は運用に従う）。**API で `main` を PR head の SHA に force 更新する操作は行わない**（履歴・レビュー・ブランチ保護との整合のため）。

## 使用例（短文）

- **docs-only checkpoint:** PR タイトルに `[docs-only]` を付ける場合は、`docs/` 以外を変えない（invariant 参照）。
- **機械判定を増やす checkpoint:** `docs/checkpoint_machine_check_items.md` の順序に従い、**1 項目ずつ** PR にする。
- **投資ロジック（Checkpoint 1）:** `docs/checkpoint1_restart_scope.md` と `PLAN.md` §3 / §13 の範囲を外れない。

## チーム承認・マージ前チェックリスト

PR を merge 候補にする前に、次を満たす（人間が最終確認）。

- [ ] **CI（必須チェック）がすべて成功**している。
- [ ] **1 PR = 1 目的**で、スコープ外の変更が混ざっていない。
- [ ] **実行したテスト / lint / pre-commit** が PR に正直に書かれている（未実行は未実行）。
- [ ] **PR #10 / PR #14 のレーン**と意図せず混ざっていない（別 checkpoint として扱う）。
- [ ] **Tiingo 系**を、この PR の目的と混ぜていない。
- [ ] rollback が説明できるサイズ（巨大な無関係リファクタがない）。

## 次の Issue / PR の粒度と順序（提案）

段階的に進めるときの **目安順**（必ずしもこの順でなければならないわけではない）。

1. **運用ドキュメントのみ** — 本書のような「型」の固定、テンプレ・invariant との整合確認。
2. **機械判定 1 項目** — `docs/checkpoint_machine_check_items.md` の「次」の 1 行だけ実装。
3. **Checkpoint 1 投資ロジック** — `PLAN.md` / `checkpoint1_restart_scope.md` に沿った **小さい実装 PR** を積む。
4. **保留中レーン** — PR #10 / PR #14、Tiingo は **別 Issue** で理由・優先度を更新してから着手（本リストに混在させない）。

## Issue / PR に書くときの短いテンプレ（コピー用）

**Issue タイトル例:** `[CP] <一行で checkpoint 名>`

**PR の冒頭に置く一文:**

> 本 PR は Issue #&lt;番号&gt; の checkpoint のみ。スコープ外: PR #10 / PR #14 / Tiingo / 無関係リファクタ。

## メモ

- 状態語（draft / hold / merged 等）は **`docs/checkpoint_state_machine.md`** に合わせる。
- 本書の更新も **小さな PR 1 本**で行い、いきなり全面書き換えしない。
