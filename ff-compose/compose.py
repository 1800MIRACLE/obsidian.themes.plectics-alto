"""Compose new Farm-Fresh icons from the set's own parts.

    python -I compose.py <FatCow_Icons16x16 dir> <FatCow_Icons32x32 dir> [--only name,name]

Reads compose.json (recipes) and parts/parts.json (from extract_parts.py).
Writes out/16/<name>.png, out/32/<name>.png and sheet.png.

A recipe is a list of ops, either shared by both sizes ("ops") or per size
("16": [...], "32": [...]). The canvas starts empty; ops run in order:

  {"op": "base", "body": "page_white"}       body of a base = the base as the set
                                             draws it under badges (parts/)
  {"op": "base", "icon": "table", "shift": [dx, dy]}   a plain set icon
  {"op": "badge", "name": "tag", "nudge": [dx, dy], "anchor": "add"}
        composite an extracted badge (straight alpha OVER). "anchor": put the
        badge's bottom-right corner where that other badge's is.
  {"op": "badge", "name": "table", "repaint": {...}}  see "pixels" below; the
        repaint is applied to the badge (in badge coordinates) before it is placed
  {"op": "copy", "from": "note", "box": [x0, y0, x1, y1], "to": [x, y],
        "mode": "over" | "replace", "flip": "h" | "v"}   copy part of a set icon
  {"op": "erase", "box": [x0, y0, x1, y1]}             make transparent
  {"op": "fill", "box": [...], "color": "note@4,5"}      fill with a sampled colour
  {"op": "slice9", "from": "note", "src": [x0, y0, x1, y1], "border": [l, t, r, b],
        "mid": [x, y], "to": [x0, y0, x1, y1]}
        a set drawing resized the pixel-art way: its corners and edges (border
        widths l, t, r, b) are kept, the middle pixel row/column "mid" repeats.
        Used to make small note cards from the note icon.
  {"op": "pick", "from": "bullet_blue", "cols": [5, 7, 8, 9, 11], "rows": [4, 5, 7, 9, 10, 11],
        "to": [x, y], "flip": "h" | "v", "transpose": true}
        a set drawing made smaller the pixel-art way: the listed source columns
        and rows are kept (a nearest-neighbour downscale chosen by hand), so the
        outline, highlight and drop shadow stay. "transpose" swaps rows and
        columns (after picking). Used for the graph balls and the canvas cards.
  {"op": "pixels", "at": [x, y], "rows": ["ab.", ".ba"], "colors": {"a": "note@4,5"}}
        hand-placed pixels; '.' keeps what is there, '_' makes it transparent.
        An opaque colour replaces the pixel; a part-transparent one (a sampled
        drop-shadow pixel) is composited over it.
        Colours are ONLY sampled from set icons: "name@x,y" (current size) or
        "name@16:x,y".

A recipe can instead say {"use_existing": "name", "why": "..."}: nothing is
written; the sheet shows the existing icon.

Boxes are [x0, y0, x1, y1) with x1, y1 exclusive.
Derived from Farm-Fresh web icons (c) FatCow Web Hosting, CC BY 3.0 US.
"""
import sys, json, pathlib, textwrap
import numpy as np
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
PARTS = HERE / "parts"
OUT = HERE / "out"


class Set:
    def __init__(self, d16, d32):
        self.dirs = {16: pathlib.Path(d16), 32: pathlib.Path(d32)}
        self.cache = {}
        self.parts = json.loads((PARTS / "parts.json").read_text())

    def icon(self, name, s):
        k = (name, s)
        if k not in self.cache:
            p = self.dirs[s] / f"{name}.png"
            if not p.is_file():
                raise SystemExit(f"no such icon: {name} ({s} px)")
            a = np.array(Image.open(p).convert("RGBA"), dtype=np.uint8)
            a[a[..., 3] == 0] = 0
            self.cache[k] = a
        return self.cache[k]

    def body(self, name, s):
        rec = self.parts["bodies"].get(name, {}).get(str(s))
        if not rec:
            raise SystemExit(f"no body for {name} at {s} px (run extract_parts.py; needs 3+ variants)")
        return np.array(Image.open(PARTS / rec["file"]).convert("RGBA"), dtype=np.uint8)

    def badge(self, name, s):
        rec = self.parts["badges"].get(name, {}).get(str(s))
        if not rec:
            raise SystemExit(f"no badge {name} at {s} px")
        return np.array(Image.open(PARTS / rec["file"]).convert("RGBA"), dtype=np.uint8), rec

    def color(self, spec, s):
        name, xy = spec.split("@")
        if ":" in xy:
            sz, xy = xy.split(":")
            s = int(sz)
        x, y = (int(v) for v in xy.split(","))
        return self.icon(name, s)[y, x].copy()


def over(dst, src, x, y):
    """alpha-composite src (h,w,4 u8, straight) onto dst at x,y (clipped)."""
    s = dst.shape[0]
    h, w = src.shape[:2]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(s, x + w), min(s, y + h)
    if x0 >= x1 or y0 >= y1:
        return
    a = src[y0 - y:y1 - y, x0 - x:x1 - x].astype(float) / 255
    b = dst[y0:y1, x0:x1].astype(float) / 255
    sa, ba = a[..., 3:4], b[..., 3:4]
    oa = sa + ba * (1 - sa)
    rgb = (a[..., :3] * sa + b[..., :3] * ba * (1 - sa)) / np.maximum(oa, 1e-9)
    out = np.clip(np.round(np.concatenate([rgb, oa], -1) * 255), 0, 255).astype(np.uint8)
    out[out[..., 3] == 0] = 0
    dst[y0:y1, x0:x1] = out


def put_pixels(img, op, st, s):
    ax, ay = op.get("at", [0, 0])
    cols = {k: st.color(v, s) for k, v in op.get("colors", {}).items()}
    for j, row in enumerate(op["rows"]):
        for i, ch in enumerate(row):
            if ch in ". ":
                continue
            x, y = ax + i, ay + j
            if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                if ch == "_":
                    img[y, x] = 0
                elif cols[ch][3] == 255:
                    img[y, x] = cols[ch]
                else:
                    over(img, cols[ch].reshape(1, 1, 4), x, y)


def run(ops, st, s):
    img = np.zeros((s, s, 4), np.uint8)
    for op in ops:
        k = op["op"]
        if k == "base":
            if "body" in op:
                img = st.body(op["body"], s).copy()
            else:
                src = st.icon(op["icon"], s)
                dx, dy = op.get("shift", [0, 0])
                img = np.zeros_like(src)
                over(img, src, dx, dy)
        elif k == "badge":
            b, rec = st.badge(op["name"], s)
            b = b.copy()
            if "repaint" in op:
                put_pixels(b, op["repaint"], st, s)
            if op.get("flip") == "h":
                b = b[:, ::-1].copy()
            x, y = rec["offset"]
            if "anchor" in op:
                _, ar = st.badge(op["anchor"], s)
                x = ar["offset"][0] + ar["size"][0] - rec["size"][0]
                y = ar["offset"][1] + ar["size"][1] - rec["size"][1]
            if "at" in op:
                x, y = op["at"]
            dx, dy = op.get("nudge", [0, 0])
            over(img, b, x + dx, y + dy)
        elif k == "copy":
            src = st.icon(op["from"], s) if "from" in op else st.body(op["from_body"], s)
            x0, y0, x1, y1 = op["box"]
            part = src[y0:y1, x0:x1].copy()
            if op.get("flip") == "h":
                part = part[:, ::-1]
            if op.get("flip") == "v":
                part = part[::-1]
            tx, ty = op.get("to", [x0, y0])
            if op.get("mode", "over") == "replace":
                h, w = part.shape[:2]
                img[ty:ty + h, tx:tx + w] = part[: s - ty, : s - tx]
            else:
                over(img, part, tx, ty)
        elif k == "slice9":
            # a resized copy of a set drawing: corners and edges kept, middle repeated
            src = st.icon(op["from"], s)
            sx0, sy0, sx1, sy1 = op["src"]
            bl, bt, br, bb = op["border"]
            mx, my = op["mid"]
            tx0, ty0, tx1, ty1 = op["to"]
            w, h = tx1 - tx0, ty1 - ty0
            part = np.zeros((h, w, 4), np.uint8)
            for j in range(h):
                sy = sy0 + j if j < bt else (sy1 - (h - j) if j >= h - bb else my)
                for i in range(w):
                    sx = sx0 + i if i < bl else (sx1 - (w - i) if i >= w - br else mx)
                    part[j, i] = src[sy, sx]
            over(img, part, tx0, ty0)
        elif k == "pick":
            src = st.icon(op["from"], s)
            part = src[np.ix_(op["rows"], op["cols"])].copy()
            if op.get("transpose"):
                part = part.transpose(1, 0, 2).copy()
            if op.get("flip") == "h":
                part = part[:, ::-1]
            if op.get("flip") == "v":
                part = part[::-1]
            over(img, part, *op["to"])
        elif k == "erase":
            x0, y0, x1, y1 = op["box"]
            img[y0:y1, x0:x1] = 0
        elif k == "fill":
            x0, y0, x1, y1 = op["box"]
            img[y0:y1, x0:x1] = st.color(op["color"], s)
        elif k == "pixels":
            put_pixels(img, op, st, s)
        else:
            raise SystemExit(f"unknown op {k}")
    return img


# ---------------------------------------------------------------- sheet

LIGHT, DARK = (0xfa, 0xfb, 0xfa, 255), (0x1e, 0x23, 0x33, 255)


def tile(a, k):
    return Image.fromarray(a, "RGBA").resize((a.shape[1] * k, a.shape[0] * k), Image.NEAREST)


def group(a16, a32, bg):
    """one icon: 16 px x4, 32 px x2, 16 px x1, 32 px x1, on bg."""
    g = Image.new("RGBA", (64 + 6 + 64 + 6 + 16 + 6 + 32, 64), bg)
    g.alpha_composite(tile(a16, 4), (0, 0))
    g.alpha_composite(tile(a32, 2), (70, 0))
    g.alpha_composite(tile(a16, 1), (140, 24))
    g.alpha_composite(tile(a32, 1), (162, 16))
    return g


def sheet(rows, st, path):
    """rows: (name, label, new16, new32, [neighbour names])"""
    gw, gap, lab = 194, 14, 190
    ncol = 1 + max(len(r[4]) for r in rows)
    pw = ncol * (gw + gap) + gap
    W = lab + 2 * pw
    rh = 64 + 26
    img = Image.new("RGBA", (W, 30 + rh * len(rows)), LIGHT)
    d = ImageDraw.Draw(img)
    d.rectangle([lab + pw, 0, W, img.height], fill=DARK)
    d.text((lab + gap, 8), "light #fafbfa: new icon (16 x4, 32 x2, 16 x1, 32 x1), then Farm-Fresh neighbours",
           fill=(40, 40, 40, 255))
    d.text((lab + pw + gap, 8), "dark #1e2333: same", fill=(220, 220, 230, 255))
    for i, (name, label, a16, a32, nb) in enumerate(rows):
        y = 30 + i * rh
        d.text((6, y + 20), name, fill=(0, 0, 0, 255))
        for li, line in enumerate(textwrap.wrap(label, 30)[:3]):
            d.text((6, y + 36 + 12 * li), line, fill=(90, 90, 90, 255))
        items = [(a16, a32, "NEW" if label != "use existing" else "existing")] + \
                [(st.icon(n, 16), st.icon(n, 32), n) for n in nb]
        for p, (bg, fg) in enumerate(((LIGHT, (60, 60, 60, 255)), (DARK, (200, 200, 210, 255)))):
            x0 = lab + p * pw + gap
            for j, (b16, b32, t) in enumerate(items):
                x = x0 + j * (gw + gap)
                img.alpha_composite(group(b16, b32, bg), (x, y))
                d.text((x, y + 66), t[:30], fill=(200, 40, 40, 255) if j == 0 else fg)
    img.save(path)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = set(a.split("=", 1)[1].split(","))
    st = Set(*args)
    spec = json.loads((HERE / "compose.json").read_text())
    rows = []
    for name, r in spec["icons"].items():
        if only and name not in only:
            continue
        nb = r.get("neighbours", [])
        if "use_existing" in r:
            e = r["use_existing"]
            rows.append((name, "use existing", st.icon(e, 16), st.icon(e, 32), nb))
            print(f"{name:24s} use existing {e}")
            continue
        imgs = {}
        for s in (16, 32):
            ops = r.get(str(s), r.get("ops"))
            imgs[s] = run(ops, st, s)
            (OUT / str(s)).mkdir(parents=True, exist_ok=True)
            Image.fromarray(imgs[s], "RGBA").save(OUT / str(s) / f"{name}.png")
        rows.append((name, r.get("recipe", ""), imgs[16], imgs[32], nb))
        print(f"{name:24s} -> out/16, out/32   ({r.get('recipe', '')})")
    sheet(rows, st, HERE / "sheet.png")
    print("sheet:", HERE / "sheet.png")


if __name__ == "__main__":
    main()
