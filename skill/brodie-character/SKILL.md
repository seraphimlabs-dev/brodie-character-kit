---
name: brodie-character
description: Draw or edit the Brodie mascot on-model for a new skill or costume (chef, sleep, cardio, etc.). Use whenever generating, editing or reviewing any Brodie image. Enforces his cream #EFE7DA body colour and locked traits, and checks output for pink drift.
---

# Brodie character

Source of truth: https://github.com/seraphimlabs-dev/brodie-character-kit (`brodie.json`).
If the repo is not on disk, clone it: `git clone --depth 1 https://github.com/seraphimlabs-dev/brodie-character-kit`.

Follow `AGENTS.md` in that repo step by step:
attach both `reference/*.png`, build the prompt from `prompt.template` + `prompt.canon`,
generate (`tools/gen_brodie.py` if GEMINI_API_KEY is set), run `tools/check_cream.py`,
fix with `tools/fix_cream.py` on colour FAIL, then visually confirm lettering, face and style.

Never ship an image that fails the cream check. Brodie is never pink.
