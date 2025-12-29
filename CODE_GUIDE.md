# TLI-Tracker — AI / Developer Guide

This document is written to help human developers and AI agents understand the repository layout, where data lives, and how to safely make changes.

## Purpose
TLI-Tracker parses Torchlight: Infinite logs to track item drops and compute earnings. This fork is configured to run standalone (no external server) with `full_table.json` as the single authoritative runtime data file.

## Key files and responsibilities
- `index.py` — Main application and UI (Tkinter). Responsibilities:
  - Read game log, detect bag initialization and changes, track drops.
  - Load `full_table.json` and use it for item names, types, and prices.
  - `apply_local_overrides()` merges missing IDs and fills missing types/names only when safe (it will not overwrite user edits in `full_table.json`).
  - `get_price_info()` parses price-check log blocks and updates `full_table.json` (only when valid samples are found).
  - UI controls: Settings, Refresh Data, Drops list. `Refresh Data` calls `apply_local_overrides()`.
  - Threading: background log reader thread (`MyThread`) reads the UE log file and invokes parsing functions.

- `full_table.json` — Authoritative runtime table for items. Each entry should contain:
  - `name` (English display name)
  - `type` (item category)
  - `price` (numeric)

  Edit this file directly to change names/prices. The app will preserve manual edits on Refresh.

- `en_id_table.json` — Optional source of English names and types (used to add missing IDs only).

- `translation_mapping.json` — Maps Chinese strings to English; used only to fill empty names in `full_table.json` if present.

- `price.json` — Deprecated/ignored in standalone mode. Do not edit for standalone workflow; `full_table.json` is authoritative.

- `update_full_table.py` — CLI helper to merge `en_id_table.json` and `translation_mapping.json` into `full_table.json`. Use to regenerate or add missing IDs. It respects existing `full_table.json` entries and will not overwrite non-empty names.

- `config.json` — App configuration. Relevant keys:
  - `opacity`: UI opacity
  - `tax`: apply tax (0/1)
  - `standalone`: if present, app behaves without network (default for this branch)

- `drop.txt` / `drops.txt` — Logs of processed drops; app appends events here.

## Important Behaviors / Safety Rules
- Never overwrite `full_table.json` names or prices without explicit user intent. `apply_local_overrides()` only *adds missing IDs* and *fills missing types/names* when the existing name is empty.
- `get_price_info()` will only write prices when valid numeric samples are parsed (no `-1` entries). It schedules a UI update for the single updated item so changes are visible immediately.
- The background price updater and any network submission were removed in standalone mode.

## How to update names & prices (recommended flow)
1. Edit `full_table.json` directly (change `name` and/or `price`).
2. In the running app: Settings → `Refresh Data` to ensure UI picks up the change (the refresh will NOT overwrite your edits).
3. Optionally run `python update_full_table.py` to merge any new IDs from `en_id_table.json` into `full_table.json` (this will also not overwrite non-empty names).

## If you must ingest external (Chinese) sources
- Keep `en_id_table.json` and `translation_mapping.json` in a `sources/` folder (optional). Use `update_full_table.py` to merge into `full_table.json`, then verify manual edits remain.

## For AI agents making automated edits
- Primary file to edit: `full_table.json`. Prefer producing small, focused diffs that change only the relevant keys for an item (avoid replacing the full file unless necessary).
- When adding new IDs, ensure `type` and `price` fields are included.
- Do not remove `last_update`, `from`, or other metadata unless you understand the side-effects. `last_update` is used for UI freshness indicators.
- If you update `full_table.json` on disk while the app is running and want the UI to reflect the change, call `apply_local_overrides()` or trigger the Refresh Data button. The app also updates the UI for parsed prices automatically.

## Developer notes & testing
- Run the app: `python index.py`
- Logs and debug: `debug_log_format()` button prints current bag state and recent relevant UE game log lines.
- If changing parsing logic, add unit tests (not present) or verify against saved UE_game.log excerpts.

## Branching & PRs
- This work is on branch `standalone-mode`. Create PRs targeting `main` with concise descriptions of behavior changes (see PR template in repo root if present).

## Contact points in code for common tasks
- Add a new UI element: modify `App.__init__` in `index.py` and wire to an event handler.
- Change how prices are parsed: `get_price_info()` near the top of `index.py`.
- Change overlay/merge behavior: `apply_local_overrides()` in `index.py` and `update_full_table.py`.

## Final notes
- The repo is intentionally simplified for standalone maintenance. Keep `full_table.json` small and human-editable; prefer direct edits there for names and prices.

---
Generated for maintainers and AI assistants to safely and quickly update the tracker.
