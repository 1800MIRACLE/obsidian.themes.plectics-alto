# Plectics Alto: typed tags — appearance options (spec, 2026-11-17)

Tag colour, shape, box and fill are user options, with the
current Plectics look as the default. These options apply to inline tags (`a.tag` in
Reading view, `.cm-hashtag` in Live Preview) and to tag chips in the
Properties box (`.multi-select-pill`, families via the Typed Notes
plugin's `data-tag-kind`).

## Families (what a tag is, from its prefix)

| Family | Matches | Default colour |
|---|---|---|
| Topic | anything without a family prefix | teal |
| Type | `type/…` (legacy `form/…`) | blue-violet |
| Status | `status/…` | amber |
| Stable | `status/stable` | green |
| Absent | `status/empty`, `status/trash` | rose |
| Meta | `meta/…` | slate grey |
| Author | `author/…` | copper |
| Custom 1–3 | prefixes the user sets in Typed Notes (plugin setting) | user-chosen |

Inline tags match by `href`. Custom prefixes only work through the plugin,
because CSS cannot compare an attribute against a setting.

## Options (Style Settings → Plectics Alto → Typed tags)

### 1. Colour
- **Colour by**: Family (default) · One colour (accent) · Ink (no colour)
- **Family colours**: one light/dark colour pair per family (themed colour pickers),
  defaulting to the values above. Includes Custom 1–3.
- **Colour applies to**: Text and frame (default) · Text only · Frame only

### 2. Shape
- **Corners**: Square (default) · Slightly rounded (3 px) · Pill (fully rounded) · Chamfered (one cut corner, the Plectics label cut)

### 3. Frame (border)
- **Frame**: Coloured (default, family colour at about 50 %) · Neutral (rule grey) · None
- **Frame weight**: 1 px (default) · 1.5 px

### 4. Fill (background)
- **Fill**: Tint (default, family colour about 8–10 %, like Obsidian's own theme) · Solid (family colour, light text: a label) · None (text only, plain)

### 5. Type
- **Face**: Mono (default for tags) · Interface (Archivo) · Same as text
- **Size**: slider, 85–110 % of the surrounding text (default 92 %)
- **The # mark**: Shown in family colour (default) · Dimmed · Hidden

### 6. Where
- **Apply to**: Inline tags and Properties chips (default) · Inline tags only
- **Tag pane and search results**: follow the same style (on, default) / plain

### 7. Presets (one picker that sets the options above)
- **Plectics**: family colours, square, coloured frame, tint, mono, # coloured
- **Obsidian**: one colour, pill, no frame, tint, interface face
- **Label**: family colours, chamfered, no frame, solid fill, interface caps
- **Plain**: family colours, no frame, no fill, text only (the old "Plain tags" toggle)
- **Custom**: whatever the individual options say

## Visual display (the picker)

Each option row in the Style Settings panel shows a live preview built from
the CURRENT settings (CSS only): a row
of sample tags, one per family (`#topic`, `#type/article`, `#status/draft`,
`#status/stable`, `#meta/home`, `#author/name`). The preset row shows all
five presets side by side as small specimen strips, with the active one marked.

## Constraints

- Defaults reproduce the current look exactly (no visual change for existing users).
- Contrast: tag text at least 4.5:1 on its fill in light and dark; the
  solid-fill preset picks light or dark text per family to pass.
- Every option is a body class or a variable, so the theme stays usable without
  Style Settings.

---

## As built (2026-11-17)

Code: `src/b-layer/84-tag-options.css` (options in section `plectics-alto`, group Typed tags) and the
Typed Notes plugin (`https://github.com/1800MIRACLE/obsidian.plugin.typed-notes`). A review
of the first picker ("too many displays at once") changed the layout from the
spec above: one Style picker, one live specimen, Custom tag groups next, every
fine option collapsed under Advanced.

### Settings, in order

| Row | id | Type | Classes / variable |
|---|---|---|---|
| Style | `plx-tgp` | class-select | `plx-tgp-path` (default) · `plx-tgp-plectics` · `plx-tgp-obsidian` · `plx-tgp-label` · `plx-tgp-plain` |
| Now (live specimen) | `plx-tg-now` | info-text, Markdown | real `a.tag`s, drawn by the real rules |
| Custom tag groups: Group 1–3 | `plx-tagu-custom-1…3` | variable-themed-color | prefixes are set in the plugin |
| Advanced (collapsed): Colour by | `plx-tg-colour` | class-select | `-style` (From style) · `-family` · `-accent` · `-ink` |
| Colour applies to | `plx-tg-apply` | class-select | `-style` · `-both` · `-text` · `-frame` |
| Corners | `plx-tg-corner` | class-select | `-style` · `-square` · `-round` · `-pill` · `-cut` |
| Frame | `plx-tg-frame` | class-select | `-style` · `-colour` · `-neutral` · `-none` |
| Frame weight | `plx-tg-fweight` | class-select | `-style` · `-1` · `-15` |
| Fill | `plx-tg-fill` | class-select | `-style` · `-tint` · `-solid` · `-none` |
| Face | `plx-tg-face` | class-select | `-style` · `-mono` · `-ui` · `-text` |
| Size | `plx-tgo-size` | slider 85–110, default 92 | `--plx-tgo-size` |
| The # mark | `plx-tg-hash` | class-select | `-style` · `-shown` · `-dim` · `-hidden` |
| Family colours | `plx-tagu-topic/type/status/stable/absent/meta/author` | variable-themed-color | `--plx-tagu-*` |
| Apply to | `plx-tg-where` | class-select | `plx-tg-where-all` (default) · `plx-tg-where-inline` |
| Tag pane follows | `plx-tg-pane` | class-toggle, default off | `plx-tg-pane` |

### How Style and Advanced combine

- **Plectics** sets nothing, so tags are drawn by `35-tags` and W14 as before.
  With defaults, the computed styles of inline tags (Reading view and Live
  Preview) and Properties chips match the old build exactly. This was
  measured on 39 properties per element, in light and in dark Blue-steel,
  with zero differences.
- **Obsidian**, **Label** and **Plain** are variable bundles (section 2).
- **Path** keeps the Plectics look and adds the split (section 4).
- **Obsidian, half** (`plx-tgp-ohalf`) is the Obsidian bundle with the part
  before the first "/" filled solidly in the family colour; the rest keeps a
  16 % tint (section 4b). It needs the plugin's span, as Path does.
- **Advanced** is an override layer. "From style" adds a class that does
  nothing. Any other value sets its variables on body after the bundles, so it
  wins over every Style, including Plectics.
- **Size**, **Family colours**, **Group colours** and **Where** apply under
  every Style.
- **A colour you never changed is not written** by Style Settings, so each
  mode keeps its own hues (light, and Blue-steel in dark).
- **The old "Plain tags" toggle** (`plx-tags-plain`, main section) now acts
  as the Plain style while Style is Plectics. Before, it gave neutral grey
  key caps, not the "plain coloured text" its description promised.

### Path style

The tag splits at its first "/": `#type` stays unshaded in ink-3, and
`/article` (`/name/surname`) is shaded with a 10 % family tint in the
family colour. The leaf is the information and the namespace is only the
filing, so the eye should land on the leaf. Tags with no "/" keep the Plectics
look.

The plugin adds only `<span class="plx-tg-rest">`; the text is unchanged.

| Surface | How the span gets there |
|---|---|
| Reading view (and the settings specimen) | markdown post processor |
| Properties chips | the existing chip pass, inside Obsidian's inner `<span>` |
| Live Preview | a CodeMirror 6 ViewPlugin with mark decorations at `Prec.lowest`, so the marks nest inside `.cm-hashtag-end` |

### Contrast (text on its own fill, minimum over all families)

Measured in Obsidian with `contrast.js`, on the probe note, in Reading view
and on Properties chips.

| Palette | Plectics | Path | Obsidian | Label | Plain |
|---|---|---|---|---|---|
| Light | 4.54 | 4.54 | 6.24 | 5.37 | 5.17 |
| Blue-steel | 6.05 | 5.48 | 5.28 | 10.05 | 7.03 |

The Graphite, Charcoal, Deck, Ink and Lab rows of the first run are gone with
those palettes: Alto's dark mode is Blue-steel only.

On a **Solid** fill the text is black or white, picked from the fill's LCH
lightness (`lch(from …)`, threshold L 50). That gives at least about 4.6:1
for any fill, including group and user colours.

### Changed from the spec, and why

- **Size:** the slider is 85–110 with default 92, as specified. But 92 means
  the current Plectics size (0.76 em inline, 11.5 px on chips), and other
  values scale from it. The spec's "% of the surrounding text" would have
  changed the default size.
- **Frame and fill strengths stay per surface:** inline tags 42 % frame and
  10 % fill, chips 50 % and 8 %. In Live Preview, Plectics draws the "#"
  grey. All three keep these Plectics values unless an Advanced option says
  otherwise.
- **Tag pane:** "follow the tag style" is **off** by default. Turned on, it
  would change the default look, which the rule "Plectics reproduces the
  current look exactly" rules out.

### Not done

- **Search results:** tags there are plain text spans with no per-tag hook.
  Nothing styles them.
- **Tag pane families:** the plugin does not mark Tag pane rows. When the pane
  follows, every row uses the Topic colour, and Path does not split there.
- **Custom tag groups in the specimen:** the specimen cannot show a group,
  because the prefixes live in the plugin.
- **"# dimmed" and "# hidden" in Reading view:** they assume a mono "#" (1ch).
  With the Interface face or "Same as text" the dimmed part can be off by a
  pixel or two.
  - Hidden makes the tag `inline-block`, so a hidden-# tag does not wrap
    inside itself.
  - Live Preview shows the "#" again on the line being edited.
- **Colour swatches:** in the Settings window, the pickers show a checkered
  (empty) swatch until a colour is set. This is Style Settings / Pickr
  behaviour in the pop-out window; the defaults are listed under each row.
- **Advanced combinations:** not every combination has a contrast
  measurement. Accent and Ink use theme tokens that are already clamped, and
  Solid is safe by construction.
