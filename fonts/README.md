# Fonts shipped with Plectics Alto

| Face | Files | Licence | Source |
|---|---|---|---|
| Alto Garamond Condensed: Regular and Italic are embedded; Medium, Bold and their italics are TTF only | `AltoGaramondCondensed-*.ttf`, web subsets in `web/` | SIL OFL 1.1, a renamed derivative of EB Garamond; `OFL-EBGaramond.txt` | built by `build/make_alto_garamond.py` |
| Archivo (interface) | `archivo/Archivo-VariableFont_wdth,wght.ttf`, subset `web/Archivo.woff2` | SIL OFL 1.1; `archivo/OFL-Archivo.txt` | Omnibus-Type/Archivo (Google Fonts) |
| PLX Caps = Nimbus Sans (Regular, Bold) | `nimbus/NimbusSans-*.otf`, web subsets in `web/` | AGPL-3.0 (`nimbus/COPYING`, `nimbus/LICENSE`) | URW++ base35 (ArtifexSoftware/urw-base35-fonts) |

The theme is GPL-3.0. All notices: `../NOTICE.md`; licence notes: `../docs/FONT-LICENCES.md`.

## Rebuild

```
python -I build/make_alto_garamond.py <folder with EB Garamond variable TTFs> .   # the six Alto Garamond TTFs
python -I build/make_web_subsets.py                                              # web/*.woff2
python -I build/gen_fontcss.py                                                   # ../src/b-layer/58-alto-fonts.css
```

## How Alto Garamond Condensed is made

Plain horizontal scaling to 80 % thins the vertical stems to 80 % while the
horizontal bars keep their weight, so the letters look uneven.
`make_alto_garamond.py` avoids this:
1. For each style it instances variable EB Garamond at a heavier weight, chosen by search (`build/stems.py`). After the 80 % squeeze, the vertical stems equal the original style's stems.
2. `build/condense.py` scales outlines, advances, kerning and mark anchors. Composite glyphs are flattened first, so they are not scaled twice.
3. `build/fix_names.py` sets the family names, the nominal weight classes (400/500/700) and the style bits.

The compensation is exact for Regular and Medium. Bold reaches stems of 116 against the original's 131, because it is limited by EB Garamond's heaviest master.
