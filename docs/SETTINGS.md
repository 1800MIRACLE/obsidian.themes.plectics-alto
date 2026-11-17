# Plectics Alto: Style Settings options

One section, **Plectics Alto** (section id `plectics-alto`), declared in `src/b-layer/69-settings6.css`. Groups appear in this order, and all start closed.

Each option sets a body class or a CSS variable.

## Text

| Option | id | Type | Default |
|---|---|---|---|
| Reading font | `plx-body-font` | select: Constantia, Georgia, Palatino Linotype, Sitka Text, EB Garamond, IBM Plex Serif, CMU Serif, CMU Concrete, IBM Plex Sans, Inter, Instrument Sans, Golos Text, Verdana | Constantia (`plx-body-constantia`) |
| Title font | `plx-display-font` | select: Alto Garamond Condensed (built in), Apple Garamond (if installed), EB Garamond | Alto Garamond Condensed (`plx-display-alto`) |
| Sans-serif headings | `plx-headings-sans` | toggle | off |
| Wider reading column | `plx-wide-lines` | toggle | off |

## Interface

| Option | id | Type | Default |
|---|---|---|---|
| Use Obsidian's accent colour | `plx-use-accent` | toggle | off |
| Classic Mac font | `plx-chicago` | select: Off (`plx-chicago-off`), Titles and alerts (`plx-chicago-titles`), Titles, menus and buttons (`plx-chicago-system7`) | Titles and alerts |
| Monospaced interface | `plx-ui-mono` | toggle | off |
| Flat buttons | `plx-flat` | toggle | off |
| Angled corners | `plx-chamfer` | toggle | off |
| Segmented sliders | `plx-slider-segmented` | toggle | off |

The Classic Mac font row is the panel's only preview: a "Window Title" plate drawn in the face the current choice gives.

## Dark mode

| Option | id | Type | Default |
|---|---|---|---|
| Metal finish | `plx6-y2k-metal` | toggle | off |

Dark mode is always **Blue-steel**, with no setting and no body class needed. The rules that used to require `.plx6-dark-y2k` now read `:not(.plx6-no-steel)`. That selector is always true and has the same specificity, so no rule changed rank. Blue-steel variations will ship as separate themes, not as a picker.

## Icons and file list

The Farm-Fresh rows exist only in **Plectics Alto Icons**, where the icons are on by default. **Plectics Alto** has no Farm-Fresh icons and no such rows. The source declares a `plx-ff` toggle; `buildvariants.py` rewrites it for each theme.

| Option | id | Type | Default |
|---|---|---|---|
| Turn colour icons off (Plectics Alto Icons only) | `plx-ff-off` | toggle | off |
| Show colour icons in (Plectics Alto Icons only) | `plx-ff-scope` | select: Files and tabs (`plx-ff-files`), Everywhere (`plx-ff-all`) | Files and tabs |
| Where Iconize set an icon (Plectics Alto Icons only) | `plx-ff-iconize` | select: Keep the Iconize icon (`plx-ff-iconize-keep`), Use the colour icon (`plx-ff-iconize-hide`) | Keep the Iconize icon |
| Hide file-type icons | `plx-no-file-icons` | toggle | off |
| Hide tree lines | `plx-no-tree-lines` | toggle | off |

## Notes and properties

| Option | id | Type | Default |
|---|---|---|---|
| Properties layout | `plx-props-layout` | select: Panel, Ledger, Strip, Margin, LCD, Tucked (`plx-props-*`) | Panel (`plx-props-panel`) |
| Properties text size | `plx-prop-fs` | slider 9.5–14 px | 13 px |
| Hide "Add property" | `plx-properties-hide-add` | toggle | off |
| Hide properties in reading view | `plx-properties-reading-hidden` | toggle | off |
| Hide the note-type label | `plx-no-kicker` | toggle | off |
| Grid paper behind notes | `plx-bg-grid` | toggle | off |
| Teal glow at the top of notes | `plx-bg-gradient` | toggle | off |

## Typed tags

| Option | id | Type | Default |
|---|---|---|---|
| Plain tags | `plx-tags-plain` | toggle | off |
| Style | `plx-tgp` | select: Plectics, Path, Obsidian coloured, Obsidian half, Label, Plain (`plx-tgp-*`) | Plectics (`plx-tgp-plectics`); applies with no class too |

Below Style come a live specimen ("Now") and four sub-groups:
- **Custom tag groups** (open): three colours; the prefixes are set in the Typed Notes plugin.
- **Advanced (overrides)** (closed): colour by, colour applies to, corners, frame, frame weight, fill, face, size, the # mark. Each defaults to "From style", which sets a do-nothing class (`plx-tg-*-style`), except Size (a slider, 92).
- **Family colours** (closed): one light and one dark (Blue-steel) colour per family.
- **Where tags are styled** (closed): Apply to (inline tags and Properties chips, or inline only) and Tag pane follows the tag style.

Tag families come from the prefixes `type/` (legacy `form/`), `status/`, `meta/` and `author/`. Tags without one are Topic. The full list, the presets and the contrast measurements are in [TAG-OPTIONS.md](TAG-OPTIONS.md).

## Canvas

| Option | id | Type | Default |
|---|---|---|---|
| Dots instead of grid | `plx-canvas-dots` | toggle | off |
| Finer grid | `plx-canvas-fine` | toggle | off |
| Hide the canvas frame | `plx-canvas-no-frame` | toggle | off |

## Removed for Alto

- **Dark palette** (`plx-dark-palette`: Graphite, Charcoal, Deck, Ink, Lab), **Cyan accent in dark mode** (`plx-dark-cyan`), and the Plectics-6 **Dark palette** choice (`plx6-dark`: Blue-steel / From Plectics). The CSS for Charcoal, Deck, Ink and Lab in `a-base/66-dark-variants.css` was removed. The Graphite tokens in `00-tokens` stay, because Blue-steel builds on them.
- The leftover rules for those palettes were removed on 2026-11-17: Lab in `81-audit-a4`, `83-audit-a5` and `84-tag-options`; Charcoal in `81`, `83` and `a-base/71-canvas`; cyan in `a-base/65-surfaces` and `71-canvas`; the "Blue-steel overrides this" chips for the palette and cyan rows in `81`. The `:not(.plx-dark-lab)` guards in `a-base/68-dark-native` are always true now; they stay to keep those rules' specificity.
- **Fonts that cannot ship** (see [FONT-LICENCES.md](FONT-LICENCES.md)): the title fonts Apple Garamond Light, VC Garamond Condensed and Ivy Journal, and the reading fonts Lab Grotesque and Univers. Their CSS in `a-base/60-plugins.css` went with them. Apple Garamond stays as a title choice, labelled "(if installed)". The interface face is now Archivo, embedded; Univers is no longer named.
- The panel extras: "dark mode only" chips, the palette strip, the Flat/Metal key previews, the line-icon and Farm-Fresh sample, the dashed scope chips, and the dimmed "cannot apply now" rows.

## With Style Settings off

The theme works without the plugin, and every default looks the same. This was checked live on 2026-11-17 by comparing the computed style of every element (note in Reading and Live Preview, file tree, canvas, tabs, status bar), in light, dark and dark with Metal, with the plugin on and off. No element differed.

- **Reading font, Title font, interface:** the base tokens are already Constantia, Alto Garamond Condensed and Archivo.
- **Properties layout:** the Panel rules read `body:not(.plx-props-ledger, .plx-props-strip, .plx-props-margin, .plx-props-lcd, .plx-props-tucked)`, so Panel applies when no layout class is set. This selector has the same specificity as the old `body.plx-props-panel`.
- **Classic Mac font:** the "Titles and alerts" rules read `body:not(.plx-chicago-off)`. This has the same specificity as the old `:is(.plx-chicago-titles, .plx-chicago-system7)`.
- **Interface kerning:** the rule that turns kerning off for the caps face also lists `body`. With the plugin, Style Settings' `plx-` classes on body had turned kerning off for the whole interface; listing `body` keeps that look without the plugin.
- **Properties text size:** the slider default is 13 px, the size the theme draws. It used to say 11.5 px, but Style Settings writes no variable for an untouched slider, so 13 px was always the size in use.
- **Tags:** the Plectics style sets nothing, so tags look the same.
