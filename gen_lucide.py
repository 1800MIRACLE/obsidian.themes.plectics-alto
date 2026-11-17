"""Emit CSS custom properties holding Lucide icons as mask data-URIs."""
import re, sys, urllib.parse, pathlib
SRC = pathlib.Path(sys.argv[1])
W = "2.4"   # 24-unit stroke -> ~1.5px at 15px
names = ["library","folder","folder-open","file","file-text","layout-dashboard","pencil-ruler",
         "table-2","file-type","image","file-audio","film","file-code","file-json","sheet","sigma","book-marked",
         "asterisk","paperclip","user-round","pin","inbox","list-tree","wrench","trash-2","construction",
         "circle-dashed","archive","layout-template","sticky-note","shield","flask-conical","history","circle-alert"]
out = []
for n in names:
    s = (SRC / f"{n}.svg").read_text(encoding="utf-8")
    s = re.sub(r"\s+", " ", s).replace("> <", "><").strip()
    s = re.sub(r' (width|height)="24"', "", s)
    s = s.replace('stroke="currentColor"', 'stroke="#000"').replace('stroke-width="2"', f'stroke-width="{W}"')
    s = s.replace(" />", "/>").replace(" >", ">").replace(' class="lucide"', "")
    s = s.replace('"', "'")
    enc = urllib.parse.quote(s, safe=" =:/,.'-_()")
    out.append(f'  --plx-ico-{n}: url("data:image/svg+xml,{enc}");')
print("\n".join(out))
