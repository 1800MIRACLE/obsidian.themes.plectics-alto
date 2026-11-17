"""Re-make the web subsets in fonts/web/ that 58-alto-fonts.css embeds.

    python -I fonts/build/make_web_subsets.py

Coverage: Latin-1, Latin Extended-A, general punctuation, arrows, minus and a
few marks (the code points listed in UNICODES). All name records are kept, so
the copyright and licence fields (name IDs 0, 13, 14) travel with each subset.
Archivo is pinned to width 100 (the wdth axis would triple the size) and keeps
its weight axis, 100-900.
Then run gen_fontcss.py.
"""
import os, subprocess, sys, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
F = lambda *p: os.path.join(ROOT, "fonts", *p)
UNICODES = ("U+0020-007E,U+00A0-017F,U+0192,U+01FA-01FF,U+0218-021B,U+02C6-02C7,U+02C9,U+02D8-02DD,"
            "U+0394,U+03A9,U+03BC,U+03C0,U+2013-2014,U+2018-201A,U+201C-201E,U+2020-2022,U+2026,U+2030,"
            "U+2039-203A,U+2044,U+20AC,U+2122,U+2190-2193,U+2202,U+2206,U+220F,U+2211-2212,U+2215,"
            "U+2219-221A,U+221E,U+222B,U+2248,U+2260,U+2264-2265,U+25CA,U+FB01-FB02")
JOBS = [  # (source, output, layout features)
    (F("AltoGaramondCondensed-Regular.ttf"), "AltoGaramondCondensed-Regular", "kern,liga,pnum"),
    (F("AltoGaramondCondensed-Italic.ttf"), "AltoGaramondCondensed-Italic", "kern,liga,pnum"),
    (F("nimbus", "NimbusSans-Regular.otf"), "NimbusSans-Regular", "kern,liga"),
    (F("nimbus", "NimbusSans-Bold.otf"), "NimbusSans-Bold", "kern,liga"),
    (F("archivo", "Archivo-VariableFont_wdth,wght.ttf"), "Archivo", "kern,liga,pnum,tnum"),
]
tmp = tempfile.mkdtemp()
for src, name, feats in JOBS:
    if name == "Archivo":
        pinned = os.path.join(tmp, "Archivo-wdth100.ttf")
        instancer.instantiateVariableFont(TTFont(src), {"wdth": 100}).save(pinned)
        src = pinned
    out = F("web", name + ".woff2")
    subprocess.run([sys.executable, "-I", "-m", "fontTools.subset", src, "--unicodes=" + UNICODES,
                    "--layout-features=" + feats, "--name-IDs=*", "--name-languages=*",
                    "--flavor=woff2", "--output-file=" + out], check=True)
    print(f"{name:32s} {os.path.getsize(out):7d} B")
