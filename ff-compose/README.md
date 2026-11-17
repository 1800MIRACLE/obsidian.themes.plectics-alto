# ff-compose

New Farm-Fresh icons for Plectics Alto Icons, made from the set's own parts (bodies, corner badges and pieces of set icons), at 16 and 32 px.

Icons derived from Farm-Fresh web icons © FatCow Web Hosting, CC BY 3.0 US (https://creativecommons.org/licenses/by/3.0/us/).

## Outputs

| Path | What |
|---|---|
| `out/16/<name>.png`, `out/32/<name>.png` | the new icons (RGBA) |
| `sheet.png` | contact sheet: each new icon at 16 ×4, 32 ×2, 16 ×1 and 32 ×1, next to its nearest Farm-Fresh neighbours, on #fafbfa and #1e2333 |
| `new-icons-20261117.png` | old vs new for graph view, local graph and canvas, and the two other new icons (Publish, unique note), at 1× and enlarged, on light and dark |
| `parts/{16,32}/<badge>.png` | extracted corner badges (straight alpha), offsets in `parts/parts.json` |
| `parts/{16,32}/body_<base>.png` | a base as the set draws it under its badges |
| `parts/parts.json` | index: badge offset and size, source pairs, rebuild error; body sources |

## The icons

Thirteen icons are composed. The theme maps twelve of them; `canvas_board` is kept but no longer mapped. One more entry, `page_white_draw`, uses an existing set icon.

| New name | Recipe |
|---|---|
| `kanban_board` | `layouts_three_grid` (grey 3-column frame) + six note cards, 3 / 2 / 1 per column. The cards are the `note` icon cut down by `slice9` (its own corners, edges and fill). |
| `link_incoming` | `link` body + `back` badge (the `go` badge mirrored). The mirror of `link_go`. |
| `canvas_board` | `node` (its elbow connectors), with its three balls replaced by small `note` cards (`slice9`, with the note's own drop shadow). Replaced in the theme by `canvas_cards`; kept here, not mapped. |
| `page_white_footnote` | `page_white_text`; the last text lines become a footnote: the red superscript "1" copied from `insert_footnote`, then a short text line (and at 32 px a short rule above it). |
| `page_white_properties` | `page_white` body + `tag` badge (from `layer_label`). |
| `table_properties` | `table` body + `tag` badge. |
| `folder_template` | `folder_table`, with the grid in its table badge repainted as a layout (header, sidebar, green content block), in colours sampled from `layout_content`. |
| `page_white_template` | `page_white` body + `table` badge, repainted as a layout in the same way. |
| `page_white_draw` | **use existing `page_white_paintbrush`**. The set already has a page with a brush badge (`page_white_paint` is the same idea), so no new icon is made. |
| `graph_network` | Graph view (tab `graph`, ribbon `lucide-git-fork`). Five `bullet_*` balls (green, blue, orange), made smaller with `pick` so each keeps its outline, highlight and drop shadow, joined by thin links in `node`'s connector grey with `node`'s connector shadow. A mesh with a cycle (a triangle), not a tree, and no dominant node. |
| `graph_local` | Local graph (tab `localgraph`). A `bullet_purple` ball in the centre (Obsidian's accent for the active note), five grey balls from `node` (via `pick`) around it, each linked only to the centre. |
| `canvas_cards` | Canvas (tab `canvas`, ribbon `lucide-layout-dashboard`, `.canvas` files). The `layer` body (a blue checker board) with two white text cards (`text_align_left`, made smaller with `pick`, so the frame, text lines and shadow stay) and an Obsidian-style connector: a grey elbow line in `bullet_arrow_right`'s outline grey and a small down arrowhead into the second card. |
| `world_publish` | Obsidian Publish (`lucide-send`: "Publish changes" in the ribbon, "Publish file" in menus). `world` body + `get` badge (the green up arrow): upload to the web. Before, it shared `page_white_world` with the Web viewer tab. |
| `page_white_unique` | "Create new unique note" (`sheets-in-box`, the Unique note creator core plugin, which names notes by a time stamp). `page_white` body + `clock` badge. Before, it was `page_white_stack`, a pile of copies. |

Hand-placed pixels exist only in:

- the two template badges (the layout pattern), in colours sampled from `layout_content`;
- the graph links (1 px at 16, 2 px at 32), in `node`'s connector greys and shadow;
- the canvas connector line and its arrowhead (5 × 3 px at 16, 10 × 6 px at 32), in `bullet_arrow_right`'s outline and fill greys.

Everything else is set pixels: bodies, badges, and `copy`, `slice9` and `pick` of set icons. The graph links are drawn first and the balls on top, so each link ends under a ball.

## Rerun

From this folder (the library folder is passed in as data, never run):

```
set FF=<folder of the FatCow Farm-Fresh set, from https://www.fatcow.com/free-icons>
python -I extract_parts.py "%FF%\FatCow_Icons16x16" "%FF%\FatCow_Icons32x32"
python -I compose.py      "%FF%\FatCow_Icons16x16" "%FF%\FatCow_Icons32x32"
```

`extract_parts.py` takes about 15 s and rewrites `parts/`. `compose.py` reads `compose.json` and `parts/`, then writes `out/` and `sheet.png`. To add an icon, add a recipe to `compose.json`. The ops are listed at the top of `compose.py`: `base`, `badge`, `copy`, `slice9`, `pick`, `erase`, `fill`, `pixels`, and `use_existing`. `pick` keeps chosen source rows and columns (a hand-chosen nearest-neighbour downscale), which makes a 5 px ball from the 7 px `bullet_*` ball with its outline, highlight and shadow intact. A part-transparent `pixels` colour (a sampled shadow) is composited, not written over.

## What the extraction found about the set

- **Variants are not "base + badge".** FatCow redraws the base for its variants: a 16 px `page_white` moves 1 px left and gets a new dog-ear, and a 16 px folder moves 2 px up. So badges are diffed against the **body**, which is the per-pixel majority of all `X_*` variants of a base, not against `X` itself.
- **The 16 px icons are downscaled from bigger art**, so a badge is never pixel-identical on two icons: its outline and glow pick up the colour under them. A badge's pixels are medians over many icons. Edge pixels are fitted as `V = a·c + (1−a)·body` over the different bodies. `parts.json` records the rebuild error per badge. A typical badge rebuilds its source icons to within about 10–25 levels on average, and the worst single icon is off by up to about 40.
- **No hole is cut round a badge.** Each badge has a soft, part-transparent light glow (about 1 px) and a faint black shadow (alpha 30–51). Both are kept in the badge, so compositing it gives the set's own halo. No clearing step is needed.
- **Badges extracted** (both sizes unless noted): add, delete, go, edit, link, error, star, key, magnify, gear, get, put, table, page, picture, wrench, find, lightning, database, valid, information (16 only), plus:
  - `lock`: there is no `X_lock` pair. Taken from `document_protect` against `page_white` (one source; the lock is centred there, so place it with `"at"`/`"anchor"` when used as a corner badge).
  - `tag`: from `layer_label` against the layer body (one source). Leftovers of the layer frame are erased (`ERASE` in the script).
  - `clock`: from the pixels that `session_idle_time`, `sheduled_task` and `system_time` share (no base exists for any of them). It has no glow.
  - **arrows**: `go` (outgoing, right) is a real badge family with 60+ pairs. The set has no `_back` badge family: `document_back` is different art, and `door_in`/`door_out` and `arrow_*` are whole icons. So `back` (incoming, left) is the `go` badge mirrored. The set's own `bullet_back` is drawn the same way, as the go arrow pointing left with the light still from the top. `get`/`put` (up/down) exist on a few bases and are extracted too.

## Known limits

- Single-source badges (`lock`, `tag`, `table`, `page`, `picture`, `information`, `star` at 32) keep the colour of their source body in their semi-transparent edge pixels.
- At 16 px:
  - The kanban cards are 4×3 px, so each card is an outline ring around two yellow pixels.
  - The footnote "1" is only 3×4 px.
  - The tag badge is as big as the set's pencil badge, so it hides most of the table grid in `table_properties`.
  - The graph balls are 4–6 px, so at 1× they read as round-cornered squares with a light centre, as the set's own small balls do (`bubblechart`).
  - The canvas connector is 1 px with a 5 × 3 px arrowhead; on the blue checker board it reads, but quietly.
- At 32 px, the `clock` badge (which has no glow) is a light grey clock face, so `page_white_unique` is quieter there than at 16 px.
