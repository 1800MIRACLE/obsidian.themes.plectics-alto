"""Extract Farm-Fresh corner badges by diffing base/variant pairs.

    python -I extract_parts.py <FatCow_Icons16x16 dir> <FatCow_Icons32x32 dir>

Writes, next to this script:
    parts/{16,32}/<badge>.png          badge RGBA (straight alpha), cropped
    parts/{16,32}/body_<base>.png      a base as it is drawn UNDER its badges
    parts/parts.json                   index: offsets, sources, fit quality

What the set does (measured by this script; numbers in parts.json)
  * A variant is not "base + badge". FatCow redraws the base for its variants:
    a 16 px page moves 1 px left and gets a redrawn dog-ear, a 16 px folder
    moves 2 px up. So badges are diffed against the BODY, not the base.
  * The 16 px icons are downscaled from bigger art, so one badge is never
    pixel-identical on two icons (outline and glow pixels pick up the colour
    under them). Values are therefore medians over many icons, and edge
    pixels are fitted as  V = a*c + (1-a)*body  over the different bodies.
  * The set does not cut a hole round its badges. Each badge has a soft light
    glow (about 1 px, part-transparent) and a faint drop shadow (black, alpha
    30-51). Both are kept in the extracted badge, so compositing it gives the
    set's own halo; no clearing step is needed.

Steps
  1. Body. For base X with 3+ variants X_*, the body is the per-pixel majority
     of the variants (each badge hides a different part, so the most common
     value is the body). Pixels every badge hides are filled from X itself at
     the shift that fits best.
  2. Badge. Each pair (body of X, X_s) is a sample. Samples are clustered by
     their opaque changed pixels (a suffix can have two drawings) and the
     biggest cluster is solved per pixel: where the body is empty the
     variant is the badge; elsewhere the median, or the least-squares
     alpha/colour fit when it explains the bodies better.
  3. Check. Every sample is rebuilt from body + badge; mean error and the
     share of pixels off by more than 24 are written to parts.json.

  Badges with no X / X_s pairs come from EXTRA (one source each, a box limits
  the diff): lock from document_protect over page_white, tag from
  layer_label over the layer body, clock from the pixels that
  session_idle_time, sheduled_task and system_time share. The incoming arrow
  "back" is the "go" badge mirrored; the set's own bullet_back / bullet_go
  pair is drawn the same way (same arrow, pointing left, lit from the top).

Derived from Farm-Fresh web icons (c) FatCow Web Hosting, CC BY 3.0 US.
"""
import sys, json, pathlib, collections
import numpy as np
from PIL import Image

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "parts"

WANTED = ["add", "delete", "go", "edit", "link", "error", "star", "key", "magnify",
          "gear", "get", "put", "table", "page", "picture", "wrench", "find",
          "lightning", "database", "valid", "information"]
# single-source badges: body to diff against (a body name, or None = the plain
# base at a fixed shift) and a box per size [x0, y0, x1, y1] holding the badge
EXTRA = {
    "lock": {"body": None, "base": "page_white", "variant": "document_protect",
             "shift": {"16": [0, 0], "32": [0, 0]},
             "box": {"16": [2, 4, 13, 14], "32": [6, 7, 25, 27]}},
    "tag": {"body": "layer", "base": "layer", "variant": "layer_label",
            "shift": None, "box": {"16": [3, 0, 16, 16], "32": [6, 0, 32, 32]}},
}
# leftovers of a single-source body that touch the badge (the layer frame
# around layer_label's tag): boxes [x0, y0, x1, y1) in icon coordinates
ERASE = {
    "tag": {"16": [[13, 0, 14, 3], [12, 6, 13, 7], [13, 11, 14, 12], [12, 12, 14, 13], [3, 13, 6, 14],
                    [11, 13, 14, 14], [3, 14, 7, 15], [10, 14, 14, 15]],
            "32": [[27, 9, 28, 10]]},
}
CONSENSUS = {"clock": ["session_idle_time", "sheduled_task", "system_time"]}
MIRROR = {"back": "go"}
TOL = 1  # per-channel tolerance for the exact body majority


# ---------------------------------------------------------------- helpers

def load_dir(d):
    icons = {}
    for p in sorted(pathlib.Path(d).glob("*.png")):
        a = np.array(Image.open(p).convert("RGBA"), dtype=np.uint8)
        a[a[..., 3] == 0] = 0  # transparent pixels: one value
        icons[p.stem] = a
    return icons


def shifted(a, dx, dy):
    s = a.shape[0]
    out = np.zeros_like(a)
    xs0, xs1 = max(0, -dx), min(s, s - dx)
    ys0, ys1 = max(0, -dy), min(s, s - dy)
    out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = a[ys0:ys1, xs0:xs1]
    return out


def eq(a, b, tol=TOL):
    return np.all(np.abs(a.astype(int) - b.astype(int)) <= tol, axis=-1)


def owner(name, icons):
    """longest existing prefix (on '_') that is not the name itself."""
    parts = name.split("_")
    for i in range(len(parts) - 1, 0, -1):
        b = "_".join(parts[:i])
        if b in icons:
            return b
    return None


# ---------------------------------------------------------------- bodies

def make_body(base, variants, icons):
    """the base as drawn under badges.
    Pass 1: per-pixel majority of the variants, to find the shift of the base.
    Pass 2: at each pixel take the shifted base's value if 2+ variants show it
    (the body showing through), else the majority if it is clear (a redrawn
    part, e.g. the 16 px page's dog-ear), else the shifted base (unknown)."""
    s = icons[base].shape[0]
    st = np.stack([icons[v] for v in variants])               # k,s,s,4
    code = st.view(np.uint32)[..., 0]                         # k,s,s
    k = len(variants)
    need = max(2, int(np.ceil(0.2 * k)))
    mode = np.zeros((s, s, 4), np.uint8)
    clear_mode = np.zeros((s, s), bool)
    for y in range(s):
        for x in range(s):
            vals, cnt = np.unique(code[:, y, x], return_counts=True)
            o = np.argsort(-cnt)
            if cnt[o[0]] >= need and (len(o) == 1 or cnt[o[0]] > cnt[o[1]]):
                mode[y, x] = np.frombuffer(np.uint32(vals[o[0]]).tobytes(), np.uint8)
                clear_mode[y, x] = True
    best = None
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            b = shifted(icons[base], dx, dy)
            sc = int((eq(b, mode) & clear_mode).sum()) - 2 * (abs(dx) + abs(dy))
            if best is None or sc > best[0]:
                best = (sc, dx, dy)
    fill = shifted(icons[base], best[1], best[2])
    seen = (np.abs(st.astype(int) - fill.astype(int)).max(-1) <= TOL).sum(0)  # s,s
    body = fill.copy()
    known = seen >= 2
    # a redraw may change or remove body pixels, never add new ones (that is a badge)
    # and only when most variants agree (a shared redraw, not the glow of the
    # commonest badge family)
    mcount = np.zeros((s, s), int)
    mcode = mode.view(np.uint32)[..., 0]
    mcount = (code == mcode[None]).sum(0)
    redraw = ~known & clear_mode & (mcount >= 0.4 * k) & ((fill[..., 3] > 0) | (mode[..., 3] == 0))
    body[redraw] = mode[redraw]
    known |= redraw
    return body, known, (best[1], best[2])


# ---------------------------------------------------------------- solving

DIFF = 8     # a channel must move more than this to count as changed
SAME = 24    # two badge pixels within this are "the same drawing"


def changed(a, b):
    return np.abs(a.astype(int) - b.astype(int)).max(-1) > DIFF


def over(c, a, b):
    """straight colour c (.,3) with alpha a OVER straight RGBA b (.,4); 0..1 floats."""
    ab = b[..., 3]
    oa = a + ab * (1 - a)
    rgb = (c * a[..., None] + b[..., :3] * (ab * (1 - a))[..., None]) / np.maximum(oa, 1e-9)[..., None]
    return np.concatenate([rgb, oa[..., None]], -1)


def solve(obs, s):
    """obs: list of dicts with B (body u8), K (body known), V (variant u8), D (changed).
    The 16 px set is downscaled from bigger art, so the same badge is never
    pixel-identical over two bodies: values are medians, and edge pixels are
    fitted as  V = a*c + (1-a)*B  over the different bodies.
    -> badge float RGBA straight (s,s,4)"""
    n = len(obs)
    badge = np.zeros((s, s, 4))
    B = np.stack([o["B"] for o in obs]).astype(float) / 255
    V = np.stack([o["V"] for o in obs]).astype(float) / 255
    K = np.stack([o["K"] for o in obs])
    D = np.stack([o["D"] for o in obs])
    region = D.mean(0) >= (0.5 if n > 2 else 0.01)
    for y, x in zip(*np.nonzero(region)):
        bb, vv, kk, dd = B[:, y, x], V[:, y, x], K[:, y, x], D[:, y, x]
        empty = kk & (bb[:, 3] == 0)
        if empty.any():                 # nothing under it: the variant IS the badge
            badge[y, x] = np.median(vv[empty], 0)
            continue
        c = np.median(vv[dd] if dd.any() else vv, 0)
        err_med = np.abs(over(c[:3], np.full(n, c[3]), bb) - vv).mean()
        best = (err_med, c[:3], c[3])
        use = kk
        if use.sum() >= 2 and np.ptp(bb[use], 0).max() > 0.05:
            # least squares for a and P = a*c (premultiplied) over the bodies
            bu, vu = bb[use], vv[use]
            bp = bu[:, :3] * bu[:, 3:4]
            vp = vu[:, :3] * vu[:, 3:4]
            rows, rhs = [], []
            for i in range(len(bu)):
                for ch in range(3):
                    r = np.zeros(4); r[1 + ch] = 1; r[0] = -bp[i, ch]
                    rows.append(r); rhs.append(vp[i, ch] - bp[i, ch])
                r = np.zeros(4); r[0] = 1 - bu[i, 3]
                rows.append(r); rhs.append(vu[i, 3] - bu[i, 3])
            sol = np.linalg.lstsq(np.array(rows), np.array(rhs), rcond=None)[0]
            a = float(np.clip(sol[0], 0, 1))
            if a > 0.02:
                rgb = np.clip(sol[1:] / a, 0, 1)
                err = np.abs(over(rgb, np.full(n, a), bb) - vv).mean()
                if err < best[0] - 0.004:
                    best = (err, rgb, a)
        badge[y, x, :3], badge[y, x, 3] = best[1], best[2]
    return tidy(badge, V, B, D)


def dilate(m, r=1):
    out = m.copy()
    for _ in range(r):
        o = out.copy()
        o[1:] |= out[:-1]; o[:-1] |= out[1:]; o[:, 1:] |= out[:, :-1]; o[:, :-1] |= out[:, 1:]
        out = o
    return out


def components(m):
    lab = np.zeros(m.shape, int)
    n = 0
    for y, x in zip(*np.nonzero(m)):
        if lab[y, x]:
            continue
        n += 1
        stack = [(y, x)]
        lab[y, x] = n
        while stack:
            cy, cx = stack.pop()
            for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] and not lab[ny, nx]:
                    lab[ny, nx] = n
                    stack.append((ny, nx))
    return lab, n


def tidy(badge, V, B, D):
    """keep the badge drawing, its 1 px glow and its shadow; drop stray pixels
    that changed only because a body estimate was off."""
    strong = (np.abs(V - B).max(-1) > 40 / 255).mean(0) >= 0.5
    core = (badge[..., 3] >= 0.9) & strong
    lab, n = components(core)
    if n:
        sizes = np.bincount(lab.ravel())[1:]
        core = np.isin(lab, 1 + np.nonzero(sizes >= max(3, 0.25 * sizes.max()))[0])
    shadow = (badge[..., :3].max(-1) < 0.2) & (badge[..., 3] < 0.4)
    # ring pixels: the light glow, a shadow, or a colour one of its core
    # neighbours has (anti-aliasing); anything else is body showing through
    ring = dilate(core, 1) & ~core
    light = badge[..., :3].min(-1) > 0.8
    near = np.zeros_like(core)
    s = core.shape[0]
    for y, x in zip(*np.nonzero(ring)):
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < s and 0 <= nx < s and core[ny, nx] and                     np.abs(badge[y, x, :3] - badge[ny, nx, :3]).max() < 0.3:
                near[y, x] = True
    keep = core | (ring & (light | shadow | near)) | (dilate(core, 2) & shadow)
    badge[~keep] = 0
    return badge


def composite(body_u8, badge):
    b = body_u8.astype(float) / 255
    out = over(badge[..., :3], badge[..., 3], b)
    out = np.clip(np.round(out * 255), 0, 255).astype(np.uint8)
    out[out[..., 3] == 0] = 0
    return out


def rebuild(o, badge):
    """mean abs error (0..255) over the badge's pixels, share of them off by > SAME."""
    r = composite(o["B"], badge)
    d = np.abs(r.astype(int) - o["V"].astype(int)).max(-1)[badge[..., 3] > 0]
    if d.size == 0:
        return 0.0, 0.0
    return round(float(d.mean()), 1), round(float((d > SAME).mean()), 3)


def cluster(obs):
    """keep the biggest group of samples whose opaque changed pixels agree."""
    sig = [(o["D"] & (o["V"][..., 3] == 255)) for o in obs]
    n = len(obs)
    agree = np.eye(n, dtype=bool)
    for i in range(n):
        for j in range(i + 1, n):
            both = sig[i] & sig[j]
            if both.sum() < 4:
                continue
            iou = both.sum() / (sig[i] | sig[j]).sum()
            same = (np.abs(obs[i]["V"][both].astype(int) - obs[j]["V"][both].astype(int)).max(-1) <= SAME).mean()
            agree[i, j] = agree[j, i] = iou >= 0.6 and same >= 0.75
    seed = int(agree.sum(1).argmax())
    return [i for i in range(n) if agree[seed, i]]


def in_corner(d, s):
    """a badge sample: something changed, (almost) nothing in the top-left corner."""
    if not d.any():
        return False
    ys, xs = np.nonzero(d)
    return int(((xs < s * 0.35) & (ys < s * 0.35)).sum()) <= 3  # a few strays are tidied away


# ---------------------------------------------------------------- output

def save_part(badge, name, s, rec):
    a8 = np.clip(np.round(badge * 255), 0, 255).astype(np.uint8)
    a8[a8[..., 3] == 0] = 0
    m = a8[..., 3] > 0
    if not m.any():
        return None
    ys, xs = np.nonzero(m)
    x0, x1, y0, y1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    d = OUT / str(s)
    d.mkdir(parents=True, exist_ok=True)
    Image.fromarray(a8[y0:y1, x0:x1], "RGBA").save(d / f"{name}.png")
    rec.update({"file": f"{s}/{name}.png", "offset": [int(x0), int(y0)],
                "size": [int(x1 - x0), int(y1 - y0)]})
    return rec


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sets = {16: load_dir(sys.argv[1]), 32: load_dir(sys.argv[2])}
    assert set(sets[16]) == set(sets[32]), "the two sizes must have the same names"
    index = {"source": "Farm-Fresh web icons (c) FatCow Web Hosting, CC BY 3.0 US",
             "model": "icon = badge OVER body; body = the base as drawn under badges "
                      "(body_<name>.png), badge = straight-alpha RGBA placed at offset",
             "badges": {}, "bodies": {}, "missing": []}
    names = sorted(sets[16])
    variants = collections.defaultdict(list)
    for n in names:
        o = owner(n, sets[16])
        if o:
            variants[o].append(n)

    for s, icons in sets.items():
        S = str(s)
        bodies = {}

        def body(b):
            if b not in bodies:
                vs = variants.get(b, [])
                if len(vs) >= 3:
                    bodies[b] = make_body(b, vs, icons)
                else:
                    bodies[b] = (icons[b].copy(), np.ones((s, s), bool), (0, 0))
            return bodies[b]

        def sample(B, K, v, label, box=None):
            V = icons[v]
            D = changed(B, V) | (~K & (V[..., 3] > 0))
            if box:
                m = np.zeros((s, s), bool)
                m[box[1]:box[3], box[0]:box[2]] = True
                D &= m
            return {"B": B, "K": K, "V": V, "D": D, "pair": label}

        def finish(name, obs, seen, note=None):
            badge = solve(obs, s)
            for x0, y0, x1, y1 in ERASE.get(name, {}).get(S, []):
                badge[y0:y1, x0:x1] = 0
            errs = [rebuild(o, badge) for o in obs]
            rec = {"pairs": [o["pair"] for o in obs], "samples_seen": seen,
                   "mean_rebuild_error": max(e for e, _ in errs),
                   "worst_share_off_by_24": max(f for _, f in errs)}
            if note:
                rec["note"] = note
            rec = save_part(badge, name, s, rec)
            index["badges"].setdefault(name, {})[S] = rec
            print(f"  {name:12s} {len(obs):3d}/{seen:3d} samples  err {rec['mean_rebuild_error']:5.1f} "
                  f"off {rec['worst_share_off_by_24']:.3f}  box {rec['offset']}+{rec['size']}")

        print(f"[{s}px]")
        for name in WANTED:
            pairs = [(v[: -len(name) - 1], v) for v in names
                     if v.endswith("_" + name) and owner(v, icons) == v[: -len(name) - 1]]
            obs = []
            for b, v in pairs:
                B, K, _ = body(b)
                o = sample(B, K, v, f"{b} -> {v}")
                if in_corner(o["D"], s):
                    obs.append(o)
            if not obs:
                index["missing"].append(f"{name} @{s}")
                print(f"  {name:12s} no usable pair")
                continue
            if len(obs) == 1:
                finish(name, obs, 1, "single source: semi-transparent edge pixels keep the "
                                     "colour of the body under them")
                continue
            keep = cluster(obs)
            finish(name, [obs[i] for i in keep], len(obs))

        for name, e in EXTRA.items():
            if e["body"]:
                B, K, _ = body(e["body"])
            else:
                dx, dy = e["shift"][S]
                B, K = shifted(icons[e["base"]], dx, dy), np.ones((s, s), bool)
            o = sample(B, K, e["variant"], f"{e['body'] or e['base']} -> {e['variant']}", e["box"][S])
            finish(name, [o], 1, "single source: semi-transparent edge pixels keep the "
                                 "colour of the body under them")

        for name, srcs in CONSENSUS.items():
            yy, xx = np.mgrid[0:s, 0:s]
            corner = (xx >= s * 0.4) & (yy >= s * 0.4)
            ref = icons[srcs[0]].astype(int)
            al = [ref]
            for n in srcs[1:]:  # align each source's corner to the first one
                a = icons[n]
                best = max(((((np.abs(shifted(a, dx, dy).astype(int) - ref).max(-1) <= SAME // 2)
                              & corner & (ref[..., 3] > 0)).sum(), dx, dy)
                            for dx in range(-2, 3) for dy in range(-2, 3)))
                al.append(shifted(a, best[1], best[2]).astype(int))
            st = np.stack(al)
            agree = (np.abs(st - st[0]).max(-1) <= SAME // 2).all(0) & (st[0][..., 3] > 0)
            agree &= corner
            lab, n_ = components(agree)
            if n_:
                agree = lab == 1 + int(np.bincount(lab.ravel())[1:].argmax())
            badge = np.zeros((s, s, 4))
            badge[agree] = np.median(st, 0)[agree] / 255
            rec = save_part(badge, name, s, {"pairs": [f"shared by {n}" for n in srcs],
                            "note": "pixels three icons with different bodies share"})
            index["badges"].setdefault(name, {})[S] = rec
            print(f"  {name:12s} shared pixels of {len(srcs)} icons  box {rec['offset']}+{rec['size']}")

        for name, src in MIRROR.items():
            g = index["badges"][src][S]
            Image.open(OUT / g["file"]).transpose(Image.FLIP_LEFT_RIGHT).save(OUT / S / f"{name}.png")
            index["badges"].setdefault(name, {})[S] = {
                "file": f"{S}/{name}.png", "offset": g["offset"], "size": g["size"],
                "pairs": [], "note": f"the {src} badge mirrored left-right in its own box"}
            print(f"  {name:12s} = {src} mirrored")

        for b, (B, K, sh) in sorted(bodies.items()):
            if len(variants.get(b, [])) >= 3:
                Image.fromarray(B, "RGBA").save(OUT / S / f"body_{b}.png")
                index["bodies"].setdefault(b, {})[S] = {
                    "file": f"{S}/body_{b}.png", "from_variants": len(variants[b]),
                    "unknown_pixels": int((~K).sum()), "base_shift": list(sh)}

    (OUT / "parts.json").write_text(json.dumps(index, indent=1))
    print("wrote", OUT / "parts.json", "| badges:", len(index["badges"]),
          "| bodies:", len(index["bodies"]), "| missing:", index["missing"])


if __name__ == "__main__":
    main()
