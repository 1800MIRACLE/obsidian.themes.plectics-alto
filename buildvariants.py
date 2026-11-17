"""Make the two shipped themes from one build of Plectics Alto.

    python -I buildalto.py [flags]                    # builds dist/theme.css, then calls make()
    python -I buildvariants.py [--test-only | --to VAULT | --dist-only]   # from an existing dist/

  Plectics Alto        no Farm-Fresh icons: section 63 and the three icon
                       option rows are removed (about 290 KB lighter).
  Plectics Alto Icons  Farm-Fresh colour icons ON without Style Settings.
                       The icon rules are rewritten from `body.plx-ff` to
                       `body:not(.plx-ff-off)`; the option row becomes
                       "Turn colour icons off". Scope and Iconize rows stay.

Output: dist/variants/<theme>/{theme.css,manifest.json}, then installed.
"""
import argparse, datetime, json, pathlib, re, shutil, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import buildalto as B  # noqa: E402

ICON_ROWS = ("plx-ff", "plx-ff-scope", "plx-ff-iconize")


def drop_section(css, name):
    """Remove one source file's block (marker comment up to the next marker)."""
    m = re.search(r"/\* ---- [ab]-[a-z]+/" + re.escape(name) + r" ---- \*/.*?(?=/\* ---- [ab]-[a-z]+/|\Z)", css, re.S)
    if not m:
        sys.exit(f"section {name} not found")
    return css[:m.start()] + css[m.end():]


def yaml_row(css, row_id):
    """Span of a Style Settings row `  -\\n    id: <row_id>` up to the next row."""
    m = re.search(r"\n  -\n    id: " + re.escape(row_id) + r"\n.*?(?=\n  -\n|\n\*/)", css, re.S)
    if not m:
        sys.exit(f"settings row {row_id} not found")
    return m


def plain(css):
    css = drop_section(css, "63-farmfresh.css")
    for r in ICON_ROWS:
        m = yaml_row(css, r)
        css = css[:m.start()] + css[m.end():]
    return css


def icons(css):
    css = re.sub(r"body:not\(\.plx-ff\)", "body.plx-ff-off", css)
    css = re.sub(r"body\.plx-ff(?![-\w])", "body:not(.plx-ff-off)", css)
    m = yaml_row(css, "plx-ff")
    row = ("\n  -\n    id: plx-ff-off\n    title: Turn colour icons off\n"
           "    description: This theme shows Farm-Fresh 16 px colour icons (FatCow, CC BY 3.0 US). "
           "Turn on for the plain line icons.\n    type: class-toggle\n    default: false")
    css = css[:m.start()] + row + css[m.end():]
    css = css.replace("Used when Colour icons is on. ", "").replace("Used when Colour icons is on.", "")
    left = re.findall(r"body\.plx-ff(?![-\w])", css)
    if left:
        sys.exit(f"{len(left)} body.plx-ff selectors left")
    return css


def make(src, targets):
    for theme, fn in (("Plectics Alto", plain), ("Plectics Alto Icons", icons)):
        css = fn(src)
        if B.balance(css) != 0:
            sys.exit(f"{theme}: braces off")
        man = dict(B.MANIFEST, name=theme)
        d = B.DIST / "variants" / theme
        d.mkdir(parents=True, exist_ok=True)
        (d / "theme.css").write_text(css, encoding="utf-8", newline="\n")
        (d / "manifest.json").write_text(json.dumps(man, indent="\t"), encoding="utf-8", newline="\n")
        print(f"{theme:22s} {len(css.encode()):9d} B")
        # release copies at the repository's own paths: root = Plectics Alto, themes/<name>/ = the rest
        rel = HERE if theme == "Plectics Alto" else HERE / "themes" / theme
        rel.mkdir(parents=True, exist_ok=True)
        shutil.copy(d / "theme.css", rel / "theme.css")
        shutil.copy(d / "manifest.json", rel / "manifest.json")
        for v in targets:
            t = v / ".obsidian" / "themes" / theme
            t.mkdir(parents=True, exist_ok=True)
            if (t / "theme.css").exists() and (t / "theme.css").read_bytes() != (d / "theme.css").read_bytes():
                bk = t / "_backup"; bk.mkdir(exist_ok=True)
                (bk / f"theme-{datetime.datetime.now():%Y%m%d-%H%M%S}.css").write_bytes((t / "theme.css").read_bytes())
                for x in sorted(bk.glob("theme-2*.css"))[:-10]:
                    x.unlink()
            shutil.copy(d / "theme.css", t / "theme.css")
            shutil.copy(d / "manifest.json", t / "manifest.json")
            print("  ->", t)


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group()
    g.add_argument("--test-only", action="store_true")
    g.add_argument("--dist-only", action="store_true")
    g.add_argument("--to", type=pathlib.Path, metavar="VAULT")
    a = p.parse_args()
    targets = [x for x in (B.TEST_VAULT, B.REAL_VAULT) if x is not None]
    if a.test_only:
        if B.TEST_VAULT is None:
            p.error('--test-only needs a "test" vault in vaults.local.json')
        targets = [B.TEST_VAULT]
    if a.dist_only: targets = []
    if a.to is not None: targets = [a.to]
    make((B.DIST / "theme.css").read_text(encoding="utf-8"), targets)


if __name__ == "__main__":
    main()
