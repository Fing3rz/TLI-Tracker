#!/usr/bin/env python3
"""update_full_table.py

Force-apply local overrides into full_table.json so the app can be updated while running.
- overlays: en_id_table.json, translation_mapping.json
- writes a backup full_table.json.bak before replacing
- produces a minimal full_table.json containing only {name,type,price}

Note: price.json is ignored in the standalone build. Edit `full_table.json` directly
to change prices.

Usage: python update_full_table.py
"""
import json
import os
import shutil

ROOT = os.path.dirname(__file__)
FULL = os.path.join(ROOT, "full_table.json")
EN = os.path.join(ROOT, "en_id_table.json")
TRANS = os.path.join(ROOT, "translation_mapping.json")

if not os.path.exists(FULL) and not os.path.exists(EN):
    print("Neither full_table.json nor en_id_table.json found. Nothing to do.")
    raise SystemExit(1)

# Load base data (prefer existing full_table.json, otherwise build from en_id_table)
if os.path.exists(FULL):
    with open(FULL, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    with open(EN, "r", encoding="utf-8") as f:
        en = json.load(f)
    data = {k: {"name": v.get("name", ""), "type": v.get("type", ""), "price": 0} for k, v in en.items()}

# Overlay en_id_table.json — only add missing ids and fill missing types; do NOT overwrite existing names/prices
if os.path.exists(EN):
    try:
        with open(EN, "r", encoding="utf-8") as f:
            en = json.load(f)
        for item_id, en_entry in en.items():
            if item_id not in data:
                data[item_id] = {"name": en_entry.get("name", ""), "type": en_entry.get("type", ""), "price": en_entry.get("price", 0) if isinstance(en_entry, dict) else 0}
            else:
                # only fill missing type
                if not data[item_id].get("type") and en_entry.get("type"):
                    data[item_id]["type"] = en_entry.get("type")
    except Exception as e:
        print("Warning: failed to overlay en_id_table.json:", e)

# Apply translation mapping: zh -> en
if os.path.exists(TRANS):
    try:
        with open(TRANS, "r", encoding="utf-8") as f:
            trans = json.load(f)
        for item_id, entry in data.items():
            cur_name = entry.get("name", "")
            # Only translate if name is empty or contains CJK characters
            if not cur_name or any('\u4e00' <= ch <= '\u9fff' for ch in cur_name):
                if cur_name in trans:
                    entry["name"] = trans[cur_name]
    except Exception as e:
        print("Warning: failed to apply translation_mapping.json:", e)

# Note: prices are taken from full_table.json directly. If you want to update prices,
# edit full_table.json itself; price.json is no longer used by the standalone build.

# Produce minimal structure (strip unrelated fields)
minimal = {}
for item_id, entry in data.items():
    minimal[item_id] = {
        "name": entry.get("name", ""),
        "type": entry.get("type", ""),
        "price": float(entry.get("price", 0) or 0)
    }

# Backup and write
try:
    if os.path.exists(FULL):
        shutil.copyfile(FULL, FULL + ".bak")
except Exception:
    pass

with open(FULL, "w", encoding="utf-8") as f:
    json.dump(minimal, f, ensure_ascii=False, indent=2)

print(f"Updated {FULL} with {len(minimal)} entries (backup at {FULL}.bak if present)")
print("You can run this while the app is running to force the UI to pick up translations/prices.")
