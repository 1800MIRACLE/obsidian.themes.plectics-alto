"""Measure stem thickness (in font units) of a glyph at mid-height (vertical stem)
and the horizontal bar thickness, by rasterising at large size."""
import sys
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from PIL import Image, ImageDraw, ImageFont
import io

def stems(font_bytes, upm, size=1000):
    f = ImageFont.truetype(io.BytesIO(font_bytes), size)
    out = {}
    # vertical stem: 'l' at 45% of x-height region; horizontal: 'H' crossbar
    for ch, mode in (("l", "v"), ("n", "v"), ("H", "h"), ("e", "h")):
        img = Image.new("L", (1400, 1400), 0)
        ImageDraw.Draw(img).text((100, 100), ch, fill=255, font=f)
        px = img.load(); w, h = img.size
        bbox = img.getbbox()
        if not bbox: continue
        x0, y0, x1, y1 = bbox
        if mode == "v":
            y = y0 + int((y1 - y0) * 0.55)
            runs, cur = [], 0
            for x in range(x0, x1 + 1):
                if px[x, y] > 127: cur += 1
                elif cur: runs.append(cur); cur = 0
            if cur: runs.append(cur)
            out[ch] = max(runs) * upm / size if runs else None
        else:
            x = x0 + int((x1 - x0) * 0.5)
            runs, cur = [], 0
            for y in range(y0, y1 + 1):
                if px[x, y] > 127: cur += 1
                elif cur: runs.append(cur); cur = 0
            if cur: runs.append(cur)
            out[ch] = (sorted(runs)[len(runs)//2] if runs else None) and min(runs) * upm / size
    return out

def instance_bytes(varpath, wght):
    vf = TTFont(varpath)
    inst = instancer.instantiateVariableFont(vf, {"wght": wght})
    b = io.BytesIO(); inst.save(b); return b.getvalue()

if __name__ == "__main__":
    var = sys.argv[1]
    upm = TTFont(var)["head"].unitsPerEm
    for w in map(float, sys.argv[2:]):
        print(w, {k: round(v, 1) for k, v in stems(instance_bytes(var, w), upm).items() if v})
