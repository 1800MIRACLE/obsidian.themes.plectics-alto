"""Make "Alto Garamond Condensed": EB Garamond (SIL OFL 1.1) scaled to 80 % width.

    python -I condense.py <EBGaramond-Regular.ttf> <out.ttf> [factor] [style name]

OFL 1.1 allows modified versions under a different name; EB Garamond declares no
Reserved Font Name, and the copyright + OFL notice are kept. Glyph outlines,
advance widths, side bearings and GPOS kerning/positioning x-values are scaled.
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen

src, out = sys.argv[1], sys.argv[2]
k = float(sys.argv[3]) if len(sys.argv) > 3 else 0.8
style = sys.argv[4] if len(sys.argv) > 4 else "Regular"
from fontTools.pens.recordingPen import DecomposingRecordingPen
f = TTFont(src)
orig_gs = TTFont(src).getGlyphSet()   # untouched copy: composites are flattened from it
glyf = f["glyf"]
for name in f.getGlyphOrder():
    rec = DecomposingRecordingPen(orig_gs)
    orig_gs[name].draw(rec)            # components resolved, so nothing is scaled twice
    pen = TTGlyphPen(None)
    rec.replay(TransformPen(pen, (k, 0, 0, 1, 0, 0)))
    g = pen.glyph()
    glyf[name] = g
hmtx = f["hmtx"]
for name, (adv, lsb) in list(hmtx.metrics.items()):
    g = glyf[name]
    g.recalcBounds(glyf)
    new_lsb = g.xMin if g.numberOfContours != 0 and hasattr(g, "xMin") else round(lsb * k)
    hmtx.metrics[name] = (round(adv * k), new_lsb)
# GPOS: scale x placements/advances (kerning, mark positioning)
def scale_vr(vr):
    if vr is None: return
    for a in ("XPlacement", "XAdvance"):
        if hasattr(vr, a) and getattr(vr, a): setattr(vr, a, round(getattr(vr, a) * k))
def scale_anchor(an):
    if an is not None and hasattr(an, "XCoordinate"): an.XCoordinate = round(an.XCoordinate * k)
if "GPOS" in f:
    for lk in f["GPOS"].table.LookupList.Lookup:
        for st in lk.SubTable:
            t = st.ExtSubTable if lk.LookupType == 9 else st
            for attr in ("Value", "Value1", "Value2"): scale_vr(getattr(t, attr, None))
            for ps in getattr(t, "PairSet", []) or []:
                for pvr in ps.PairValueRecord: scale_vr(pvr.Value1); scale_vr(pvr.Value2)
            for c1 in getattr(t, "Class1Record", []) or []:
                for c2 in c1.Class2Record: scale_vr(c2.Value1); scale_vr(c2.Value2)
            for vr in getattr(t, "Value", []) if isinstance(getattr(t, "Value", None), list) else []: scale_vr(vr)
            for rec in getattr(t, "EntryExitRecord", []) or []: scale_anchor(rec.EntryAnchor); scale_anchor(rec.ExitAnchor)
            for arr in ("MarkArray", "Mark1Array"):
                ma = getattr(t, arr, None)
                if ma:
                    for r in ma.MarkRecord: scale_anchor(r.MarkAnchor)
            ba = getattr(t, "BaseArray", None)
            if ba:
                for r in ba.BaseRecord:
                    for an in r.BaseAnchor: scale_anchor(an)
            m2 = getattr(t, "Mark2Array", None)
            if m2:
                for r in m2.Mark2Record:
                    for an in r.Mark2Anchor: scale_anchor(an)
            la = getattr(t, "LigatureArray", None)
            if la:
                for att in la.LigatureAttach:
                    for cr in att.ComponentRecord:
                        for an in cr.LigatureAnchor: scale_anchor(an)
f["hhea"].advanceWidthMax = max(a for a, _ in hmtx.metrics.values())
f["OS/2"].xAvgCharWidth = round(f["OS/2"].xAvgCharWidth * k)
f["OS/2"].usWidthClass = 3 if k <= 0.8 else 4
fam = sys.argv[5] if len(sys.argv) > 5 else "Alto Garamond Condensed"
name = f["name"]
ps = fam.replace(" ", "") + "-" + style.replace(" ", "")
for rec in name.names:
    if rec.nameID in (1, 16): rec.string = fam
    elif rec.nameID == 4: rec.string = f"{fam} {style}"
    elif rec.nameID == 6: rec.string = ps
    elif rec.nameID == 3: rec.string = f"{ps};Plectics;2026"
    elif rec.nameID == 5: rec.string = f"Version 1.000; condensed derivative, width {int(k*100)} %"
name.setName((sys.argv[6] if len(sys.argv) > 6 else "Derived from EB Garamond (Copyright 2017 The EB Garamond Project Authors)") + " by Plectics, 2026: horizontally condensed to %d %%. Licensed under the SIL Open Font License 1.1." % int(k*100), 0, 3, 1, 0x409)
f.save(out)
print("saved", out)
