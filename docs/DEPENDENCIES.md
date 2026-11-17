# Plectics Alto: dependencies and plugins

Written 2026-11-17 from the CSS in `src/` and a live check in Obsidian 1.15.0 and 1.15.1 on a test vault. Items marked **[check]** are not verified.

## Hard dependencies

**None.** Alto is a CSS theme. It needs nothing else. The manifest says Obsidian 1.6.0 or later, but it was only tested on 1.15.x **[check]**.

Checked live on 2026-11-17 with every community plugin turned off (restricted mode). The note in Reading and Live Preview, the Panel properties, the file tree, a canvas, tabs and the status bar all render fully, in light, dark and Metal. In each mode, the computed style of every element (about 4,300) was compared with the same view with Style Settings and Typed Notes on. The only differences:

- the tag chips in Properties, which lose their family colours (see Typed Notes below);
- the plugin's 12 `plx-tg-rest` spans, which are gone;
- the estimated height of the two Reading views. Obsidian re-renders them when the plugin unloads; this was not investigated further.

Fonts are not dependencies either:

- Alto Garamond Condensed (titles), Archivo (interface) and PLX Caps (caps labels, Nimbus Sans) are embedded.
- Every other face is named with fallbacks: Constantia (Windows) for reading, ChicagoFLF then PLX Caps for window titles (profile page titles: ChicagoFLF then Archivo), Berkeley Mono or IBM Plex Mono then Consolas for code.

The look with only the shipped faces is the intended fallback, not a broken state.

## Soft dependencies

### Style Settings (`obsidian-style-settings`)

- **Without it:**
  - every default holds: Constantia reading text, Alto Garamond Condensed titles, the Panel properties layout, Chicago "Titles and alerts", the Plectics tag style, Blue-steel in dark mode;
  - checked live: the computed styles were identical with the plugin on and off, in light, dark and Metal.
- **With it:** the options in one section, **Plectics Alto** (seven groups, listed in [SETTINGS.md](SETTINGS.md)). Among them:
  - reading and title fonts;
  - the Metal finish;
  - where Farm-Fresh icons show (Plectics Alto Icons);
  - five other properties layouts;
  - tag styles and colours;
  - canvas grid options.

  Each option is a body class or a CSS variable, so a choice also keeps working if the plugin is removed later, until the class is gone.

### Typed Notes (companion plugin, not yet published)

Obsidian draws Properties tags as plain chips, so CSS cannot tell `#status/draft` from `#author/name` there.

- **Without it:**
  - inline tags in notes (Reading and Live Preview) are still coloured by family, because the CSS reads the tag's `href` and CodeMirror's `cm-tag-*` classes;
  - in Properties, every tag chip is drawn in the neutral ink colour, checked live;
  - the **Path** and **Obsidian, half** styles show no split, because they need the plugin's `<span class="plx-tg-rest">`;
  - custom tag groups never apply.
- **With it:**
  - Properties chips get their family colours: type, status, author, meta, topic;
  - Path and Obsidian, half split a tag at its first `/`;
  - a note's `title` property is shown as its title (this part can be turned off);
  - the three custom groups (prefixes set in the plugin, colours set in Style Settings › Typed tags) apply.

  It has no network access and writes only its own `data.json`.

### Iconize (`obsidian-icon-folder`)

The theme draws its own file-type icons in the tree (Lucide masks). Where Iconize has set an icon, Iconize's icon replaces the theme's and is sized and aligned to the row (`a-base/20-file-tree.css`).

Conflict with the Farm-Fresh icons of **Plectics Alto Icons** (`63-farmfresh.css`): both draw row, tab and title icons. The option **Where Iconize set an icon** decides:

- **Keep the Iconize icon** (default): rows with an Iconize icon show it, and all other rows show Farm-Fresh.
- **Use the colour icon:** Iconize's row, tab and title icons are hidden and Farm-Fresh draws everywhere.

Caveat: Iconize emoji icons are plain text, so the theme cannot tell them from an unresolved icon name. Iconize is not installed in this project's test vault, so none of this was checked live here **[check]**.

### Fonts the user may install

- **ChicagoFLF** (public domain): the classic Mac face for window titles and alerts. Without it, those titles use PLX Caps and the layout does not move.
- **Seven Segment:** the Widgets clock face and the world-clock readouts. It falls back to the mono face.

These are optional. The theme names them but does not ship them.

## Plugins the theme styles

Derived from the CSS. "Live" means checked in Obsidian on this project's scratch vault. "Not live here" means not checked live in this project. The `60-plugins.css` rules were written against installed copies of those plugins, before this check. "Source only" means the CSS header says the class names were read from the plugin's shipped `styles.css` and source (the 62 header lists the versions).

| Plugin | Where | What the theme does | Checked |
|---|---|---|---|
| Style Settings | 60, 69, 90 | its own panel: group boxes, keys, the Chicago preview plate | live |
| Typed Notes | 35, 84, 91 | family colours on chips, the split at /, display titles | live |
| Core Bases | a-base 70 §1 | toolbar keys, wikitable, group chips, cards, list register, embedded base | not live here |
| Core Canvas | a-base 71 | wall and grid, stepped frame, cards, group signage, edges, docked trays | live |
| Advanced Canvas | 70 §3, 71, 70-qa-y2k, 80 | collapsible-group key; dashed and dotted edge styles kept over the theme's solid edges; outline, thin and diamond arrowheads; read-only canvases | not live here |
| Iconize | 20, 63, 81 | icon replaces the type icon; Farm-Fresh precedence | not live here |
| File Explorer Note Count | 20 | `data-count` as a small LCD readout | not live here |
| File Tree Alternative **[check]** (classes `oz-explorer-*`) | 20, 68-dark-native | root strip, counts | not in the 60 header; origin **[check]** |
| Recent Files | 20 | rows in the tree language | not live here |
| Callout Copy Buttons | 40, 10 | button excluded from the key style | not live here |
| Homepage | 60 | command pills as keys | not live here |
| Widgets | 60 | clock as a seven-segment readout | not live here |
| Tag Wrangler, Multi-Tag, core Tag pane | 60, 84 | mono tag names and counts; optional "follow the tag style" | not live here |
| Excalidraw | 60 | chrome only (islands, toolbar); the drawing is untouched | not live here |
| Agent Client | 60, 80 | chat input and messages in the UI face | not live here |
| Kanban | 60, 62, 67 | lanes as cases, Chicago lane titles | not live here; deepened from source |
| Calendar | 60, 62, 67 | month header in Chicago, day grid | not live here; deepened from source |
| Dataview | 62 | result tables as wikitables, result counts in mono | source only |
| Tasks | 62 | group headings as labels with counts; field chips; due today amber, overdue red; edit modal | source only |
| Templater | 62 | `<% %>` commands marked as not-yet-existing text (amber, dashed); prompt and suggester modals | source only |
| Git | 62 | diff colours, commit message well, status letters as chips, history view | source only |
| Advanced Tables | 62 | toolbar button labels in the caps face | source only |
| Copilot | 62 | user vs assistant messages, input well | source only |
| Smart Connections | 62 | result rows, score as a mono readout | source only |
| TaskNotes | 62 | its `--tn-*` tokens mapped to the theme; open/done marks; agenda; calendar views | source only |
| QuickAdd | 62 | choice icons, highlight, file suggester selection | source only |
| Omnisearch | 62 | result titles, folder path and extension | source only |
| Editing Toolbar | 62 | toolbar as keys (beats the plugin's `#id` selectors) | source only |
| Outliner | 62 | list guides like the tree connectors; dashed teal drop target | source only |
| Plectics Canvas HUD | 71 | readout docked in the canvas frame's bottom rail | not re-checked in Alto |
| Plectics Instruments | 60 | radius hook only; its styles ship with the plugin | not re-checked in Alto |
| Plectics World Clock | 60 | `.plx-clocks` row of seven-segment displays | not re-checked in Alto |

## Recommendations

Grouped by purpose. Each says which theme feature it pairs with or which gap it fills.

### Maths

- **Latex Suite** (`artisticat1/obsidian-latex-suite`): fast LaTeX typing, with snippets ("sqx" → `\sqrt{x}`), auto-fractions, matrix shortcuts, conceal and inline-math preview. It pairs with:
  - the theme's maths-first page: CMU Serif as a reading font "matches LaTeX maths", and display maths is slightly enlarged in the CMU face (30-reading);
  - the `equation` callout, numbered (01) at the right.

  Latex Suite works in the editor only, so it does not touch the theme's styles.
- **LaTeX-like Theorem & Equation Referencer** (formerly Math Booster, `RyotaUshio/obsidian-latex-theorem-equation-referencer`): theorem environments, automatic equation numbering and "clever" cross-references (with MathLinks).
  - **Gap it fills:** the theme numbers theorem, lemma, definition, hypothesis, equation and figure callouts with CSS counters (`counter(plx-thm)` and others in 40-callouts). Those numbers are per note, only visual, and cannot be linked to. The plugin gives real, referenceable numbers.
  - **Overlap [check]:**
    - the plugin draws its own theorem callouts and can style them; whether the theme's theorem look applies to them, or both numbers show, is not tested;
    - its README notes that callout maths rendering is moving to a separate plugin, "Better Math in Callouts & Blockquotes".

    Try it on a test note first, and keep either the theme's CSS numbers or the plugin's, not both.

### Citations

- **Citations** (`hans/obsidian-citation-plugin`): reads a BibTeX/BibLaTeX or CSL-JSON export (for example Zotero with Better BibTeX). It opens or creates a literature note per reference from your title and content templates, inserts links to literature notes, and inserts Pandoc-style citations.
- **Zotero Integration** (`mgmeyers/obsidian-zotero-desktop-connector`): imports citations, bibliographies, notes and PDF annotations straight from Zotero. It needs the Better BibTeX add-on.

Pick one. Both pair with the theme's academic callouts: `references` / `bibliography` (numbered [n], hanging indent), `cite`, `quote`, `citation-needed` and the hatnotes. A literature-note template can emit those callouts so imported references are typeset by the theme. Whether either plugin's own modals need styling is **[check]**: the theme has no rules for them.

### Structure

- **Core Bases** (built in): the theme styles it more fully than any plugin (a-base `70-views` §1): an instrument toolbar of keys, wikitable rows, condensed-caps group chips, card plates, a list register, and a framed embedded base. Bases also needs no community plugin, which keeps the vault at zero hard dependencies.
- **Folder Notes** (`LostPaul/obsidian-folder-notes`): attaches a note to a folder, so clicking the folder name opens it. It fits the theme's tree, which already treats folders as library divisions (prefix glyphs, root strip). The theme has **no rules** for Folder Notes' classes, so how its marked folders look in the Plectics tree is **[check]**.

### Quality

- **Linter** (`platers/obsidian-linter`): keeps front matter tidy. The relevant rules are `format-tags-in-yaml`, `move-tags-to-yaml`, `dedupe-yaml-array-values` and `sort-yaml-array-values`. Moving tags into the `tags` property is what lets Typed Notes colour them as chips.
  - **Correction to the brief:** Linter has **no built-in rule** that enforces tag prefixes such as `type/` or `status/`; none of the YAML rules in its README does. It normalises tags; it does not check their families. Whether its custom regex replacement option could rewrite stray tags is not covered by the README **[check]**. Otherwise, fix stray tags with Tag Wrangler's rename, or find them with a saved search for tags without a known prefix.

### Canvas

- **Advanced Canvas** (`Developer-Mike/obsidian-advanced-canvas`): edge path styles (dotted, short-dashed, long-dashed), arrow styles (triangle outline, thin triangle, diamond, circle and more), flowchart node shapes, collapsible groups, portals and a read-only mode. The theme draws these:
  - solid edges by default, but a style chosen in Advanced Canvas always wins (71 §5, 70-qa-y2k §3);
  - outline arrowheads are hollow (80);
  - collapsible groups get an integrated collapse key in the group's signage band (71 §4);
  - read-only canvases are marked (70 §3).

  The theme's semiotics give the dashes a meaning: dashed is provisional, dotted is a reference.

## Companion Plectics plugins

| Plugin | What it does | Ready for public release? |
|---|---|---|
| **Typed Notes** (1.0.0) | Marks each tag chip and inline tag with its family, for Properties colours, the split styles and custom groups. Shows the `title` property as the note's title. | **Nearly.** Ten regression tests pass, and it has a README, a LICENSE and no network access. Missing: a release with its files attached. |
| **Plectics Display Title**, **Canvas HUD**, **World Clock**, **Instruments** | Title from a property; a canvas readout; seven-segment world clocks; plots and toy models. The theme has a few rules for them (`.plx-canvas-hud`, `.plx-clocks`). | **Not yet published.** Each needs a LICENSE, a public README and a release. Canvas HUD uses Canvas internals that can break between Obsidian versions. |

Before any of them is submitted: one author (1800MIRACLE) and one licence (GPL-3.0, matching the theme).
