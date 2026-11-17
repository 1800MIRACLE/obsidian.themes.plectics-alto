"""Build Alto Garamond Condensed with COMPENSATED scaling.

Plain horizontal scaling to 80 % thins vertical stems to 80 % while horizontal
bars keep their weight, so the letters look uneven. Here each style starts from
a heavier instance of variable EB Garamond, chosen so that after the 80 %
squeeze the vertical stems equal the original style's stems again.

    python -I make_alto_garamond.py <EB_Garamond folder> <out folder> [factor]

Needs: EBGaramond-VariableFont_wght.ttf and EBGaramond-Italic-VariableFont_wght.ttf
(SIL OFL 1.1). Output fonts are renamed "Alto Garamond Condensed" (OFL rule).
"""
import io, os, subprocess, sys, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stems as S

src_dir, out_dir = sys.argv[1], sys.argv[2]
k = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
STYLES = [  # (style name, original weight, italic?)
    ("Regular", 400, False), ("Medium", 500, False), ("Bold", 700, False),
    ("Italic", 400, True), ("Medium Italic", 500, True), ("Bold Italic", 700, True),
]

def inst(var, w):
    f = instancer.instantiateVariableFont(TTFont(var), {"wght": w})
    b = io.BytesIO(); f.save(b); return b.getvalue()

def vstem(b):
    m = S.stems(b, 1000)
    return (m.get("l") or 0 + m.get("n") or 0)

report = []
for style, w0, it in STYLES:
    var = os.path.join(src_dir, "EBGaramond-Italic-VariableFont_wght.ttf" if it else "EBGaramond-VariableFont_wght.ttf")
    axis = TTFont(var)["fvar"].axes[0]
    lo, hi = float(w0), float(axis.maxValue)
    target = vstem(inst(var, w0)) / k          # stem the heavier instance must have
    if vstem(inst(var, hi)) < target:
        w = hi                                 # cannot fully compensate: use the heaviest
    else:
        for _ in range(14):
            mid = (lo + hi) / 2
            if vstem(inst(var, mid)) < target: lo = mid
            else: hi = mid
        w = round((lo + hi) / 2)
    tmp = os.path.join(tempfile.gettempdir(), f"altogar-{style.replace(' ', '')}.ttf")
    open(tmp, "wb").write(inst(var, w))
    out = os.path.join(out_dir, "AltoGaramondCondensed-" + style.replace(" ", "") + ".ttf")
    subprocess.run([sys.executable, "-I", os.path.join(HERE, "condense.py"), tmp, out, str(k), style,
                    "Alto Garamond Condensed",
                    "Derived from EB Garamond (Copyright 2017 The EB Garamond Project Authors)"], check=True,
                   capture_output=True)
    after = S.stems(open(out, "rb").read(), 1000)
    orig = S.stems(inst(var, w0), 1000)
    report.append(f"{style:14s} source wght {w:5.0f}  vertical stem {after.get('l', 0):5.1f} (orig {orig.get('l', 0):5.1f})  "
                  f"H bar {after.get('H', 0):4.1f} (orig {orig.get('H', 0):4.1f})")
    os.remove(tmp)
print("\n".join(report))
subprocess.run([sys.executable, "-I", os.path.join(HERE, "fix_names.py"), os.path.dirname(os.path.dirname(HERE))], check=True)
