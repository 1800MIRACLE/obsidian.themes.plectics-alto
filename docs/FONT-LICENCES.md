# Plectics Alto: fonts and their licences

Checked 2026-11-17 against the name table of each font file and the licence
files in `fonts/`. This is not legal advice. Full notices: `NOTICE.md`.

There are two separate questions:
1. **Naming** a font in the CSS (`font-family: "Berkeley Mono"`) is always allowed. The font is used only if the user has it installed.
2. **Shipping** a font (embedded `@font-face` data) is allowed only when its licence permits redistribution.

## Shipped (embedded in theme.css)

| Role | Font | Licence | Files |
|---|---|---|---|
| Titles, h1/h2 (default) | **Alto Garamond Condensed**, a derivative of EB Garamond at 80 % width, weight-compensated and renamed | SIL OFL 1.1 (EB Garamond has no Reserved Font Name) | `fonts/AltoGaramondCondensed-*.ttf`, `fonts/OFL-EBGaramond.txt`, built by `fonts/build/make_alto_garamond.py` |
| Interface | **Archivo**, weights 100–900, width 100 | SIL OFL 1.1 | `fonts/archivo/`, `fonts/archivo/OFL-Archivo.txt` |
| Caps labels ("PLX Caps") | **Nimbus Sans** Regular and Bold, urw-base35 | AGPL-3.0. The font exception covers only PostScript and PDF, so the full AGPL applies. It combines with the theme's GPL-3.0 under section 13. | `fonts/nimbus/` (OTF, COPYING, LICENSE) |

The embedded copies are subsets in `fonts/web/`, made by `fonts/build/make_web_subsets.py`. All name records are kept, including copyright and licence.
`fonts/build/gen_fontcss.py` writes them into `src/b-layer/58-alto-fonts.css`.

## Named only, used if installed

| Role | Stack, in order | Notes |
|---|---|---|
| Reading text | Constantia → CMU Serif → IBM Plex Serif → Georgia | Constantia is a Windows system font. CMU and Plex are OFL and free to install. |
| Small text (properties, footnotes, captions) | IBM Plex Serif → Georgia | |
| Code and data | Berkeley Mono → IBM Plex Mono → JetBrains Mono → Fragment Mono → Consolas | Berkeley Mono is commercial (U.S. Graphics). It is used only if you own and install it. |
| Serif headings h3/h4 | EB Garamond → Garamond → Palatino Linotype → Georgia | |
| System face (title bars, graph labels) | ChicagoFLF → Chicago → PLX Caps | ChicagoFLF is public domain (Robin Casady). It is not shipped, so install it to use it. |
| Title option | Apple Garamond, labelled "(if installed)" | Commercial; not shipped |

## Not used

Some fonts were removed from the public build because they cannot ship and are
not system fonts:
- Univers: commercial; Archivo replaces it;
- Lab Grotesque and Ivy Journal: commercial;
- VC Garamond Condensed: no licence information;
- Apple Garamond Light.

ITC Garamond was the first wish for the condensed title face. It is commercial and cannot be modified and shipped, so EB Garamond was used instead.

## Not shipped yet

`fonts/` also holds Medium, Bold and their italics of Alto Garamond Condensed,
as TTF for desktop use. The theme embeds Regular and Italic only; heavier
weights in the theme are synthesised.
