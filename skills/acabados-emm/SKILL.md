---
name: acabados-emm
description: "Acabados_EMM (by ElMasMelo): makes the finishing assets of a Minecraft mod — sound effects (local Python synthesis + Freesound CC0), item/block icons 16x16 and the mod logo 128x128 — from the mod folder's entrada/ASSETS.md, and drops them in entrada/. Use on acabados-emm, 'sonidos del mod', 'iconos del mod', 'logo del mod'."
---

# Acabados_EMM

You make **sounds, icons and the logo** for a mod. No mod code, no 3D models (those are `/mod-creator-emm` and `/mob-creator-emm`).
Reply in the user's language (default Spanish).

## Input: the mod folder
- Ask for (or detect in cwd) the mod folder that has `entrada/ASSETS.md` (written by `/mod-creator-emm`).
- Read **only** `ASSETS.md`, and only rows of type `sonido`, `icono`, `logo` with state `pendiente` (or the ids the user names). Don't read the plan or the code.
- No ASSETS.md? Ask the user for a short list (id + what it is) and create `entrada/ASSETS.md` with the table format from `/mod-creator-emm` (`references/plantilla.md` §4).
- Music only if the row says `musica` or the user asks; otherwise effects only.

## Files
- `references/sonidos.md` — read for sound rows.
- `references/iconos.md` — read for icon/logo rows.
- `scripts/sfx.py`, `scripts/freesound.py`, `scripts/pixel.py` — run them, don't rewrite them. `python <script> --help` lists options.
Scripts live in the `scripts/` folder next to this SKILL.md; pass absolute output paths.

## Requirements (check once, before the first script)
- Python 3 with `numpy scipy pillow` (`python -c "import numpy, scipy, PIL"`; if it fails, offer `pip install numpy scipy pillow`).
- `ffmpeg` on PATH (for .ogg). If missing, tell the user how to install it for their OS and stop the sounds group.
- Optional: `FREESOUND_API_KEY` env var (free key at freesound.org/apiv2/apply). Without it, use synthesis only. Never ask the user to paste the key in the chat.

## Flow
1. **One round (`AskUserQuestion`, max 4):** which groups now (sonidos · íconos · logo), source for voices (Freesound for animal/creature voices, synthesis for the rest — Recommended), variants per sound (3 Recommended).
2. **Make in batches**, one group at a time: all sounds of one mob, or all icons, at once.
3. **Approval in the chat** (never in another app's panel): send the files with `SendUserFile` (sounds playable, icons as PNG scaled ×8 preview), ask in one question: approve · redo <id>.
4. On approval: final files in `entrada/sonidos/`, `entrada/texturas/`, `entrada/logo/`; set those rows to `listo` in `ASSETS.md`.
5. **Close:** write `entrada/sonidos/sounds.json` (fragment ready to merge, with `subtitle` keys) and `entrada/sonidos/subtitulos_es_en.json` (lang keys es/en). Show one line per group: done / pending.

## Token rules
- Batch everything; never one tool call per file when a loop does it.
- Don't listen/inspect audio by reading it: trust the script output (duration/format), the user judges by ear.
- Web search or downloads: only after the user says yes (Freesound downloads list name, author, license and duration first).
- Credits for every downloaded sound go to `entrada/sonidos/CREDITS.md` (the script does it).
