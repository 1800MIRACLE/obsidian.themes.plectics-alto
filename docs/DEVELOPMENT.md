# Plectics Alto: building and layout

## Build

```
python -I buildalto.py               dist/ (+ the vaults in vaults.local.json, if that file exists)
python -I buildalto.py --test-only   dist/ + the "test" vault of vaults.local.json
python -I buildalto.py --dist-only   dist/ only
python -I buildalto.py --to <vault>  dist/ + that vault only
```

1. `buildalto.py` concatenates `src/a-base/*.css`, then `src/b-layer/*.css`, in name order, into `dist/theme.css`. This file holds the code of both themes. The build refuses brace mismatches and control characters. The destination flags are mutually exclusive, and bad flags fail before anything is written.
2. It then calls `buildvariants.make()`, which writes the two shipped themes to `dist/variants/`:
   - **Plectics Alto:** section 63 (the icons) and the three icon option rows are removed.
   - **Plectics Alto Icons:** the icon rules are rewritten from `body.plx-ff` to `body:not(.plx-ff-off)`, so the icons are on without Style Settings, and the option becomes "Turn colour icons off".
3. Only the two variants are installed, into `<vault>/.obsidian/themes/<theme>/`. The last ten replaced `theme.css` files are kept in `_backup/` there.

**`vaults.local.json`** is optional and is not in the repository: `{"test": "<path>", "real": "<path>"}`. Without it a plain build writes `dist/` only.

**Release files:** every build also copies Plectics Alto to `theme.css` and `manifest.json` at the root, and Plectics Alto Icons to `themes/Plectics Alto Icons/`. These are the files users install, so commit them after each build.

## Generated files

| File | Generator |
|---|---|
| `src/b-layer/58-alto-fonts.css` | `fonts/build/gen_fontcss.py`, from `fonts/web/*.woff2` (`fonts/build/make_web_subsets.py`). See [fonts/README.md](../fonts/README.md). |
| `src/b-layer/63-farmfresh.css` | `gen_farmfresh.py`, from `icons/farm-fresh/{16,32}/` and the composed icons in `ff-compose/out/` |

## Checks

- `python -m unittest test_buildalto`: build destinations, bad flags, a clone with no local vaults, the theme name, braces in every source file, and both variants (no icons in Plectics Alto; no `body.plx-ff` left in Plectics Alto Icons).

## Folder layout

| Path | What |
|---|---|
| `src/a-base/` | The Plectics base theme (tokens, workspace, file tree, notes, callouts, properties, canvas, page types). |
| `src/b-layer/` | The layer on top: shipped fonts (58), popular plugins (62), Farm-Fresh icons (63), Blue-steel dark mode and Metal (64, 65, 70), Chicago (67), the Style Settings option list (69), the control family (72), fixes (80–83), tag options (84). |
| `fonts/` | The shipped faces, web subsets in `web/`, generators in `build/`. |
| `icons/farm-fresh/` | The Farm-Fresh icons the theme uses, 16 and 32 px. |
| `ff-compose/` | The eight icons composed from Farm-Fresh parts, and the script that makes them. |
| `docs/` | [SETTINGS.md](SETTINGS.md), [TAG-OPTIONS.md](TAG-OPTIONS.md), [FONT-LICENCES.md](FONT-LICENCES.md), [DEPENDENCIES.md](DEPENDENCIES.md). |

## Options

All options are in one Style Settings section, **Plectics Alto** (id `plectics-alto`, in `src/b-layer/69-settings6.css`). See [SETTINGS.md](SETTINGS.md). Style Settings is optional: every default looks the same without it.
