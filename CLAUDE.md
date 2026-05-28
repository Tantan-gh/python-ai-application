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

## Adding a new tool

1. Create `tools/<name>.py` with a function that accepts user inputs, builds a prompt, and returns `generate(prompt)`.
2. Add an entry to the `TOOLS` dict in `app.py`.
3. Add an `elif tool == "<key>":` block in `app.py` with the Streamlit UI and the function call.
