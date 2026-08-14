# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```powershell
streamlit run app.py
```

Requires a `.env` file with `GEMINI_API_KEY=<key>` in the project root (see `.env.example`).

## Architecture

All AI generation flows through a single path:

```
app.py  →  tools/<tool>.py  →  utils/gemini_client.generate()  →  Gemini API
```

**`utils/gemini_client.py`** — sole Gemini API wrapper. Holds a module-level singleton `_model`. The `generate(prompt)` function is the only entry point used by tools. Model defaults to `gemini-1.5-flash`.

**`tools/`** — one file per writing feature. Each file exports a single function that builds a Japanese prompt string and calls `generate()`. No tool has state; they are pure prompt-builders. Constants like `PLATFORM_SPECS` (sns_writer) and `TONE_DESCRIPTIONS` (tone_converter) are defined at module level and also imported directly by `app.py` for UI options.

**`app.py`** — single-file Streamlit UI. Tool selection is driven by the `TOOLS` dict (`label → key`). Each `key` maps to an `if/elif` block that renders inputs and calls the corresponding tool function. No routing library; Streamlit re-runs the entire script on each interaction.

## Standalone pages

`spi_nonverbal.html` — SPI非言語の練習問題集。Streamlit アプリとは独立した単一ファイルの静的ページで、ブラウザで直接開いて使う（スマートフォン向けレイアウト）。問題データは末尾の `<script>` 内の `Q` 配列に `{id, cat, d, q, c, a, e, calc, tip}` 形式で定義されている（`d` は難易度 1=易 / 2=中 / 3=難、`e` は考え方、`calc` は計算、`tip` は注意点で、この3つが解説として順に表示される）。分野は同ファイル冒頭の `CATS` に定義。選択肢は `c` の5つに加えて「わからない」が常に自動で追加される（内部値 `UNKNOWN = -1`、本番モードの時間切れは `TIMEUP = -2`）。練習モード（時間制限なし・1問ごとに解説）と本番モード（1問ごとの制限時間・解説は結果画面にまとめて表示）を `mode` で切り替える。復習セッション（`reviewMode`）は累計正答率に加算しない。学習記録は `localStorage` の `spi-nonverbal-v1` に保存され、`{stats, wrong, hist}` を持つ。`hist` は問題ID→直近3回の正否（`o`/`x`/`u`）で、練習モードでのみ追記される。外部 CSS/JS/フォントは読み込まない。

## Adding a new tool

1. Create `tools/<name>.py` with a function that accepts user inputs, builds a prompt, and returns `generate(prompt)`.
2. Add an entry to the `TOOLS` dict in `app.py`.
3. Add an `elif tool == "<key>":` block in `app.py` with the Streamlit UI and the function call.
