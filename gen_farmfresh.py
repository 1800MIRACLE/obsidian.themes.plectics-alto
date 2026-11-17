"""Generate src/b-layer/63-farmfresh.css: the Farm-Fresh icons of Plectics Alto Icons.

    python gen_farmfresh.py

Icons: Farm-Fresh web icons v3.92 by FatCow Web Hosting, CC BY 3.0 US
(https://creativecommons.org/licenses/by/3.0/us/, set: https://www.fatcow.com/free-icons).
The icons this theme uses are copied into icons/farm-fresh/{16,32}/. To use a
new icon, copy its 16 px and 32 px PNGs from the FatCow set there first.
Thirteen icons are composed from Farm-Fresh parts (ff-compose/out/; twelve
are mapped here, canvas_board is kept but unused); they are derived works
under the same licence. Each icon is embedded as
image-set(16 px 1x, 32 px 2x), so plain screens get the hand-drawn 16 px
pixels and HiDPI screens the 32 px drawing.

The rules are written behind body.plx-ff. buildvariants.py rewrites that to
body:not(.plx-ff-off) for "Plectics Alto Icons" (icons on, with a "Turn colour
icons off" option) and drops this section from "Plectics Alto".

How it plugs in
  File tree   the theme draws each row icon from --plx-ico-<lucide id>
              tokens (20-file-tree.css). With plx-ff those tokens are
              re-pointed at Farm-Fresh PNGs, and the row ::before switches
              from a tinted MASK to a plain background image. Folders get
              folder-flavoured variants of the keyword icons.
  Tabs        by the tab's data-type (markdown, canvas, pdf, graph ...).
  Ribbon,     by the Lucide class Obsidian puts on the <svg> (svg.lucide-x):
  nav keys,   the svg's own paths are hidden and the PNG is its background.
  view header
  Everywhere  (plx-ff-all) the same Lucide map applied to every svg icon
              (menus, settings, buttons).

Iconize: rows that carry an Iconize icon keep it (plx-ff-iconize-keep,
default) or Iconize icons are hidden and Farm-Fresh drawn instead
(plx-ff-iconize-hide).
"""
import base64, pathlib

HERE = pathlib.Path(__file__).parent
SRC = HERE / "icons" / "farm-fresh"   # the theme's own copies of the Farm-Fresh icons it uses
D16, D32 = SRC / "16", SRC / "32"
# icons composed from Farm-Fresh parts (ff-compose/, derived works, same licence)
C16, C32 = HERE / "ff-compose" / "out" / "16", HERE / "ff-compose" / "out" / "32"


def without_text(data):
    """Keep PNG rendering chunks byte-for-byte; omit embedded editor text."""
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG")
    chunks, offset = [data[:8]], 8
    while offset < len(data):
        end = offset + 12 + int.from_bytes(data[offset:offset + 4], "big")
        if end > len(data) or end - offset < 12:
            raise ValueError("truncated PNG chunk")
        if data[offset + 4:offset + 8] not in (b"tEXt", b"zTXt", b"iTXt"):
            chunks.append(data[offset:end])
        offset = end
    return b"".join(chunks)


def png(name, size):
    a = (D16 if size == 16 else D32) / f"{name}.png"
    b = (C16 if size == 16 else C32) / f"{name}.png"
    return a if a.exists() else b
OUT = HERE / "src" / "b-layer" / "63-farmfresh.css"

# --- file-tree tokens: Lucide id (as used by 20-file-tree.css) -> Farm-Fresh
TREE = {
    "library": "books", "folder": "folder", "folder-open": "folder_page",
    "file": "page_white", "file-text": "page_white_text",
    "layout-dashboard": "canvas_cards", "pencil-ruler": "page_white_paintbrush",
    "table-2": "database_table", "file-type": "page_white_acrobat",
    "image": "picture", "file-audio": "music", "film": "film",
    "file-code": "page_white_code", "file-json": "script_code",
    "sheet": "table_excel", "sigma": "sum", "book-marked": "book_open",
    "asterisk": "asterisk_orange", "paperclip": "attach", "user-round": "user",
    "pin": "note_pin", "inbox": "inbox_document", "list-tree": "sitemap_color",
    "wrench": "wrench", "trash-2": "bin", "construction": "construction",
    "circle-dashed": "document_empty", "archive": "box_closed",
    "layout-template": "page_white_template", "sticky-note": "note", "shield": "shield",
    "flask-conical": "flask", "history": "clock_history_frame",
    "circle-alert": "error",
}
# folder rows: keyword icons become folder variants where Farm-Fresh has one
FOLDER = {
    "wrench": "folder_wrench", "user-round": "folder_user", "image": "folder_picture",
    "table-2": "folder_table", "paperclip": "folder_brick", "pin": "folder_star",
    "construction": "folder_torn", "flask-conical": "folder_lightbulb",
    "layout-template": "folder_template", "shield": "folder_key",
    "pencil-ruler": "folder_palette", "inbox": "inbox_document",
}
# tab icons by the tab header's data-type
TABS = {
    "markdown": "page_white_text", "canvas": "canvas_cards", "pdf": "page_white_acrobat",
    "image": "picture", "audio": "music", "video": "film", "bases": "database_table",
    "excalidraw": "page_white_paintbrush", "kanban": "kanban_board", "graph": "graph_network",
    "localgraph": "graph_local", "search": "magnifier", "bookmarks": "bookmark",
    "file-explorer": "folders_explorer", "recent-files": "clock_history_frame",
    "tag": "tag_hash", "backlink": "link_incoming", "outgoing-link": "link_go",
    "outline": "text_list_bullets", "footnotes": "page_white_footnote",
    "all-properties": "table_properties", "file-properties": "page_white_properties",
    "release-notes": "newspaper", "empty": "page_white", "webviewer": "page_white_world",
    "calendar": "calendar", "agent-client-chat-view": "robot",
}
# Lucide class on an <svg> -> Farm-Fresh (ribbon, nav keys, view header; and
# everywhere when plx-ff-all is on)
SVG = {
    "lucide-git-fork": "graph_network", "lucide-file-search": "page_white_magnify",
    "lucide-layout-dashboard": "canvas_cards", "lucide-files": "page_white_template",
    "lucide-terminal": "application_osx_terminal", "lucide-send": "world_publish",
    "lucide-layout-list": "database_table", "lucide-layout": "application_view_tile",
    "sheets-in-box": "page_white_unique", "dice": "dice", "homepage": "house",
    "lucide-cuboid": "bricks", "lucide-file-plus": "page_white_add",
    "excalidraw-icon": "pencil_ruler", "lucide-bot-message-square": "robot",
    "lucide-edit": "page_white_add", "lucide-folder-plus": "folder_add",
    "lucide-sort-asc": "sort_ascending", "lucide-gallery-vertical": "application_side_tree",
    "lucide-chevrons-up-down": "arrow_inout", "lucide-chevrons-down-up": "arrow_in",
    "lucide-search": "magnifier", "lucide-bookmark": "bookmark",
    "lucide-book-open": "book_open", "lucide-edit-3": "page_white_edit",
    "lucide-calendar-days": "calendar", "lucide-calendar": "calendar",
    "lucide-calendar-with-checkmark": "calendar",
}
# extra Lucide classes only for "everywhere" (menus, settings, buttons)
SVG_ALL = {
    "lucide-settings": "cog", "help": "help", "lucide-help-circle": "help",
    "lucide-trash": "bin", "lucide-trash-2": "bin", "lucide-star": "star",
    "lucide-folder": "folder", "lucide-folder-closed": "folder", "lucide-folder-open": "folder_page",
    "lucide-file": "page_white", "lucide-file-text": "page_white_text",
    "lucide-image": "picture", "lucide-link": "link", "lucide-copy": "page_white_copy",
    "lucide-lock": "lock", "lucide-unlock": "lock_open", "lucide-tags": "tag_hash",
    "lucide-tag": "tag_hash", "lucide-list": "text_list_bullets", "lucide-archive": "box_closed",
    "lucide-info": "information", "lucide-pencil": "pencil", "lucide-history": "clock_history_frame",
    "lucide-alert-triangle": "error", "lucide-ghost": "clock_history_frame",
    "lucide-book-up": "newspaper", "links-coming-in": "link_incoming", "links-going-out": "link_go",
    "lucide-file-signature": "page_white_footnote", "lucide-scissors": "cut",
    "lucide-clipboard": "paste_plain", "lucide-printer": "printer", "lucide-download": "download",
    "lucide-external-link": "page_white_go",
}


def uri(name):
    s16 = base64.b64encode(without_text(png(name, 16).read_bytes())).decode()
    s32 = base64.b64encode(without_text(png(name, 32).read_bytes())).decode()
    return (f'image-set(url("data:image/png;base64,{s16}") 1x, '
            f'url("data:image/png;base64,{s32}") 2x)')


def var(name):
    return f"var(--ff-{name})"


def main():
    used = sorted(set(TREE.values()) | set(FOLDER.values()) | set(TABS.values())
                  | set(SVG.values()) | set(SVG_ALL.values()))
    missing = [n for n in used if not png(n, 16).exists() or not png(n, 32).exists()]
    if missing:
        raise SystemExit(f"missing icons: {missing}")
    L = []
    w = L.append
    w("/* ==========================================================================")
    w("   PLECTICS ALTO · 63 · FARM-FRESH ICONS  — GENERATED by gen_farmfresh.py")
    w("   Icons: \"Farm-Fresh Web Icons\" v3.92 by FatCow Web Hosting")
    w("   (https://www.fatcow.com/free-icons), licensed CC BY 3.0 US")
    w("   (https://creativecommons.org/licenses/by/3.0/us/). Twelve of these icons are")
    w("   composed from Farm-Fresh parts (ff-compose/); they are derived works, same licence.")
    w("   In Plectics Alto Icons only: on unless Style Settings → Plectics Alto →")
    w("   Icons and file list → Turn colour icons off (body.plx-ff-off).")
    w("   Iconize also draws row/tab/title icons: see the plx-ff-iconize-* option.")
    w("   ========================================================================== */")
    w("")
    w("/* 1 · shared image values stay stable when the icon mode changes */")
    w(":root {")
    for n in used:
        w(f"  --ff-{n}: {uri(n)};")
    w("  --ff-size: 16px;")
    w("}")
    w("")
    w("body.plx-ff {")
    w("  /* the theme's row-icon tokens, re-pointed */")
    for k, v in TREE.items():
        w(f"  --plx-ico-{k}: {var(v)};")
    w("}")
    w("")
    w("/* folder rows: folder-flavoured keyword icons */")
    w("body.plx-ff .nav-files-container .nav-folder-title {")
    for k, v in FOLDER.items():
        w(f"  --plx-ico-{k}: {var(v)};")
    w("}")
    w("")
    w("""/* 2 · file tree: the row ::before becomes a picture, not a tinted mask */
body.plx-ff .nav-files-container :is(.nav-file-title, .nav-folder-title):not(:has(> .iconize-icon :is(svg, img)))::before,
body.plx-ff.plx-ff-iconize-hide .nav-files-container :is(.nav-file-title, .nav-folder-title)::before {
  content: "";
  flex: 0 0 var(--ff-size);
  width: var(--ff-size);
  height: var(--ff-size);
  margin: 0 6px 0 var(--plx-ico-lead);
  -webkit-mask: none;
          mask: none;
  background: var(--plx-row-key, var(--plx-row-sign, var(--plx-row-icon, var(--plx-ico-file)))) center / var(--ff-size) var(--ff-size) no-repeat;
  background-color: transparent !important;
  image-rendering: auto;
}
/* rows the theme greys out (META, trash, empty) stay quieter */
body.plx-ff .nav-files-container .tree-item-self:is([data-path$="empty" i], [data-path*="recycle bin" i], [data-path$="trash" i])::before {
  filter: grayscale(1) opacity(0.6);
}
/* "you are here": no teal fill behind a picture; a 1px teal frame instead */
body.plx-ff .nav-files-container .tree-item-self.is-active::before {
  background-color: transparent !important;
  outline: 1px solid var(--plx-teal);
  outline-offset: 1px;
}

/* Iconize: keep (default) — a row with an Iconize icon shows Iconize's;
   hide — Iconize's row, tab and title icons are hidden; Farm-Fresh draws. */
body.plx-ff.plx-ff-iconize-hide .nav-files-container .iconize-icon,
body.plx-ff.plx-ff-iconize-hide .iconize-title-icon,
body.plx-ff.plx-ff-iconize-hide .iconize-inline-title-wrapper > .iconize-icon,
body.plx-ff.plx-ff-iconize-hide .workspace-tab-header .iconize-icon {
  display: none !important;
}
""")
    # tabs
    w("/* 4 · tabs, by view type */")
    for t, v in TABS.items():
        w(f'body.plx-ff .workspace-tab-header[data-type="{t}"] .workspace-tab-header-inner-icon > svg.svg-icon {{ --ff-img: {var(v)}; }}')
    w("""body.plx-ff .workspace-tab-header .workspace-tab-header-inner-icon > svg.svg-icon[class] {
  background: var(--ff-img, none) center / var(--ff-size) var(--ff-size) no-repeat;
}
body.plx-ff .workspace-tab-header[data-type] .workspace-tab-header-inner-icon > svg.svg-icon {
  width: var(--ff-size);
  height: var(--ff-size);
}
body.plx-ff .workspace-tab-header[data-type] .workspace-tab-header-inner-icon > svg.svg-icon > * {
  visibility: hidden;
}
/* a tab whose type has no Farm-Fresh icon keeps its Lucide line icon */
body.plx-ff .workspace-tab-header:not(""" + ", ".join(f'[data-type="{t}"]' for t in TABS) + """) .workspace-tab-header-inner-icon > svg.svg-icon > * {
  visibility: visible;
}
""")
    # svg map
    ctx = ":is(.side-dock-ribbon, .nav-buttons-container, .workspace-tab-header-container)"
    w("/* 5 · ribbon, file-explorer keys, sidebar tab strip: by Lucide class */")
    for c, v in SVG.items():
        w(f"body.plx-ff {ctx} svg.svg-icon.{c} {{ --ff-img: {var(v)}; }}")
    sel_files = ", ".join(f"svg.svg-icon.{c}" for c in SVG)
    w(f"""body.plx-ff {ctx} :is({sel_files}) {{
  background: var(--ff-img) center / var(--ff-size) var(--ff-size) no-repeat;
  width: var(--ff-size);
  height: var(--ff-size);
}}
body.plx-ff {ctx} :is({sel_files}) > * {{ visibility: hidden; }}
""")
    # view header: only the note's own state keys (bookmark, reading/editing),
    # so a plugin's row of line-icon actions (Kanban, Excalidraw) is not mixed
    VIEW = {"lucide-bookmark": "bookmark", "lucide-book-open": "book_open", "lucide-edit-3": "page_white_edit"}
    vctx = ".view-header .view-actions"
    w("/* 5b · view header: the note's bookmark and reading/editing keys only */")
    for c, v in VIEW.items():
        w(f"body.plx-ff {vctx} svg.svg-icon.{c} {{ --ff-img: {var(v)}; }}")
    sel_v = ", ".join(f"svg.svg-icon.{c}" for c in VIEW)
    w(f"""body.plx-ff {vctx} :is({sel_v}) {{
  background: var(--ff-img) center / var(--ff-size) var(--ff-size) no-repeat;
  width: var(--ff-size);
  height: var(--ff-size);
}}
body.plx-ff {vctx} :is({sel_v}) > * {{ visibility: hidden; }}
""")
    w("/* 6 · everywhere (plx-ff-all): menus, settings, buttons, suggestions */")
    allmap = {**SVG_ALL, **SVG}
    for c, v in allmap.items():
        w(f"body.plx-ff.plx-ff-all svg.svg-icon.{c} {{ --ff-img: {var(v)}; }}")
    sel_all = ", ".join(f"svg.svg-icon.{c}" for c in allmap)
    w(f"""body.plx-ff.plx-ff-all :is({sel_all}) {{
  background: var(--ff-img) center / var(--ff-size) var(--ff-size) no-repeat;
  width: var(--ff-size);
  height: var(--ff-size);
}}
body.plx-ff.plx-ff-all :is({sel_all}) > * {{ visibility: hidden; }}
/* controls, not objects, keep their line icons: the vault switcher */
body.plx-ff.plx-ff-all .workspace-drawer-vault-switcher-icon > svg.svg-icon {{ background: none; }}
body.plx-ff.plx-ff-all .workspace-drawer-vault-switcher-icon > svg.svg-icon > * {{ visibility: visible; }}
""")
    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{OUT.name}: {len(used)} icons, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
