"""Set RIBBI and typographic names, weight class and style bits on the built fonts.

    python -I fix_names.py <theme folder>     (make_alto_garamond.py runs it last)

Regular/Italic/Bold/Bold Italic share the family "Alto Garamond Condensed";
Medium is its own RIBBI family "Alto Garamond Condensed Medium". Name IDs 16/17
group all six. usWeightClass is the nominal weight (400/500/700): the stems were
compensated to match the original style, not the heavier source instance.
"""
import glob, os, sys
from fontTools.ttLib import TTFont
root = sys.argv[1]
SPEC = {  # file style -> (nominal weight, bold, italic, RIBBI family suffix, RIBBI subfamily, typo subfamily)
    "Regular": (400, False, False, "", "Regular", "Regular"),
    "Italic": (400, False, True, "", "Italic", "Italic"),
    "Bold": (700, True, False, "", "Bold", "Bold"),
    "BoldItalic": (700, True, True, "", "Bold Italic", "Bold Italic"),
    "Medium": (500, False, False, " Medium", "Regular", "Medium"),
    "MediumItalic": (500, False, True, " Medium", "Italic", "Medium Italic"),
}
FAM = "Alto Garamond Condensed"
for f in sorted(glob.glob(os.path.join(root, "fonts", "AltoGaramondCondensed-*.ttf"))):
    style = os.path.basename(f)[len("AltoGaramondCondensed-"):-4]
    w, bold, it, suf, sub, typo = SPEC[style]
    t = TTFont(f); n = t["name"]
    ids13 = n.getDebugName(13); ids14 = n.getDebugName(14)
    for pid, eid, lid in {(r.platformID, r.platEncID, r.langID) for r in n.names}:
        n.setName(FAM + suf, 1, pid, eid, lid)
        n.setName(sub, 2, pid, eid, lid)
        n.setName(FAM + " " + typo.replace("Regular", "").strip() if typo != "Regular" else FAM + " Regular", 4, pid, eid, lid)
        n.setName(FAM, 16, pid, eid, lid)
        n.setName(typo, 17, pid, eid, lid)
        if not ids13:
            n.setName("This Font Software is licensed under the SIL Open Font License, Version 1.1.", 13, pid, eid, lid)
        if not ids14:
            n.setName("https://openfontlicense.org", 14, pid, eid, lid)
    os2 = t["OS/2"]; os2.usWeightClass = w
    sel = os2.fsSelection & ~(0x01 | 0x20 | 0x40)
    if it: sel |= 0x01
    if bold: sel |= 0x20
    if not it and not bold: sel |= 0x40
    os2.fsSelection = sel
    t["head"].macStyle = (1 if bold else 0) | (2 if it else 0)
    if "post" in t: t["post"].italicAngle = t["post"].italicAngle
    t.save(f)
    print(style, "|", n.getDebugName(1), "|", n.getDebugName(2), "|", n.getDebugName(4), "|", n.getDebugName(16), "|", n.getDebugName(17), "| wt", os2.usWeightClass, bin(os2.fsSelection), t["head"].macStyle, "| 13/14", bool(n.getDebugName(13)), bool(n.getDebugName(14)))
