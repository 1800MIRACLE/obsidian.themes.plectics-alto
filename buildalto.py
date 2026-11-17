"""Build Plectics Alto (the public-release line, cloned from Plectics-6.7 on 2026-11-17).

    python -I buildalto.py              -> dist/ (+ the vaults in vaults.local.json, if any)
    python -I buildalto.py --test-only  -> dist + the "test" vault of vaults.local.json
    python -I buildalto.py --dist-only  -> dist only
    python -I buildalto.py --to <vault> -> dist + that vault only

dist/theme.css is the whole source (both themes' code). buildvariants.make()
then writes the two shipped themes, "Plectics Alto" and "Plectics Alto Icons",
to dist/variants/ and installs those two (never dist/theme.css itself).
vaults.local.json (optional, not in the repo) lists this machine's vaults:
    {"test": "<path to a test vault>", "real": "<path to your vault>"}

Standalone: src/a-base/*.css (a frozen copy of main Plectics, 2026-11-15) then
src/b-layer/*.css (the Plectics-6 layer, now Alto's own). Nothing outside this
folder feeds the build. If backupalto.py is present (the maintainer's copy), each
build also writes a versioned backup.
"""
import argparse, pathlib, shutil, sys, json, re, datetime

HERE = pathlib.Path(__file__).parent
PARTS = [HERE / "src" / "a-base", HERE / "src" / "b-layer"]
DIST = HERE / "dist"
LOCAL = HERE / "vaults.local.json"


def _local_vault(key):
    if not LOCAL.exists():
        return None
    try:
        p = json.loads(LOCAL.read_text(encoding="utf-8")).get(key)
    except ValueError as e:
        sys.exit(f"{LOCAL.name} is not valid JSON: {e}")
    return pathlib.Path(p) if p else None


TEST_VAULT = _local_vault("test")
REAL_VAULT = _local_vault("real")
THEME = "Plectics Alto"
MANIFEST = {"name": THEME, "version": "0.1.0", "minAppVersion": "1.6.0",
            "author": "1800MIRACLE", "authorUrl": "https://plectics.org/"}


def balance(text):
    t = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    t = re.sub(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', '""', t)
    return t.count("{") - t.count("}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--test-only", action="store_true")
    destination.add_argument("--dist-only", action="store_true")
    destination.add_argument("--to", type=pathlib.Path, metavar="VAULT")
    args = parser.parse_args()
    targets = [v for v in (TEST_VAULT, REAL_VAULT) if v is not None]
    if args.test_only:
        if TEST_VAULT is None:
            parser.error('--test-only needs a "test" vault in vaults.local.json')
        targets = [TEST_VAULT]
    if args.dist_only: targets = []
    if args.to is not None: targets = [args.to]
    parts, ok = [], True
    for d in PARTS:
        for f in sorted(d.glob("*.css")):
            text = f.read_text(encoding="utf-8")
            b = balance(text)
            if any(ord(ch) < 32 and ch not in (chr(9), chr(10), chr(13)) for ch in text):
                print(f"   ! control character in {f.name}"); ok = False
            print(f" {d.name[0]} {f.name:34s} {len(text):8d} B  braces {'ok' if b == 0 else 'OFF BY %+d' % b}")
            ok &= b == 0
            parts.append(f"/* ---- {d.name}/{f.name} ---- */\n{text}\n")
    if not ok:
        sys.exit("brace mismatch - not built")
    css = "\n".join(parts)
    DIST.mkdir(exist_ok=True)
    (DIST / "theme.css").write_text(css, encoding="utf-8", newline="\n")
    (DIST / "manifest.json").write_text(json.dumps(MANIFEST, indent="\t"), encoding="utf-8", newline="\n")
    print(f"built {len(css)} bytes")
    sys.path.insert(0, str(HERE)); import buildvariants
    buildvariants.make(css, targets)
    if (HERE / "backupalto.py").exists():
        try:
            sys.path.insert(0, str(HERE)); import backupalto
            backupalto.snapshot(auto=True)
        except Exception as e:
            print("backup skipped:", e)


if __name__ == "__main__":
    main()
