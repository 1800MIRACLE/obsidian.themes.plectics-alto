# Plectics Alto: guide

Plectics Alto is a light and dark theme for Obsidian, made for research notes with mathematics. Its look combines three things: a Casio scientific instrument, a Xerox PARC workstation and an academic wiki.

`v0.1.0 · 2026-11-17`

> [!abstract]
> The interface around a note is drawn as an instrument: gray casing, raised keys, recessed fields, a status line with readouts. The note itself is drawn as a page of a textbook: Garamond titles, a serif reading face, ruled tables, numbered theorems. Every colour, line style and small mark has one fixed meaning. The theme adds about sixty callout types, page layouts chosen by a `cssclasses` value, and tag colours by family.

## 01. What it is

The theme follows one rule: **the chrome is the instrument, the note page is a textbook.** Chrome means everything around the note: ribbon, tabs, sidebars, menus, dialogs, status bar. Lamps, key caps and display panels belong there only. Inside a note, everything stays typeset. A theorem never looks like a button, and a button never looks like a paragraph.

The theme has three kinds of surface.

| Surface | What it is | Looks like |
|---|---|---|
| Case | chrome: tab strip, ribbon, sidebars, status line | cool gray casing with raised keys |
| Paper | the note | near-white page (light), lit glass (dark) |
| Display | the active row, readouts, measurements | pale teal LCD (light), lamp or phosphor (dark) |

**Light mode** is a paper document on a pale gray case. The identity colour is teal `#0A5C59`.

**Dark mode** is not light mode inverted. It is a lit page set into a darker bezel, so the case is darker than the page, as on a real device. State is shown by lamps (a lit edge, a glowing label) and not by filled cells. Dark mode has one palette, **Blue-steel**: blue-grey steel chrome in the Y2K manner. An optional **Metal finish** turns bars and keys into brushed, bevelled steel.

Other properties of the design: rows are dense (24 px tree rows), rules are 1 px, corners are square or 3–4 px, and nothing is pill-shaped.

## 02. The semiotic standard

The theme implements a small visual standard. If an element carries no meaning, it is drawn in ink or rule gray.

### Colour

| Colour | Means | Never used for |
|---|---|---|
| Teal | identity, a link, the active thing, "you are here" | decoration, warnings |
| Slate | chrome labels, title bands | emphasis in content |
| Red | error, failure, a destructive action, a link to a page that does not exist yet | "important" |
| Amber | caution, draft, provisional, needs a decision | errors |
| Blue | a selection range, information | links |
| Green | success, verified, stable | identity |
| Violet (low chroma) | formal objects: the theorem family | chrome |
| Yellow highlight | text that the reader marked | status |

### Line style

Line style shows how settled a thing is.

| Line | Means | Examples |
|---|---|---|
| solid, 1 px | fact, boundary, settled | panels, tables |
| double | a closed formal object | definition, theorem, the rule under a title |
| dashed | provisional, unresolved, not yet existing | conjecture, draft, a link to a missing page |
| dotted | a pointer to another place | internal links, property rows, reference lists |
| hatched fill | absent, empty, cancelled | stub, cancelled task, an empty note |

### Marks

| Mark | Means |
|---|---|
| ■ | complete, proven. A proof ends with ∎ |
| □ | open, to do: conjectures, exercises, unchecked tasks |
| ⊞ / ⊟ | folded / unfolded. The same pair marks every fold in the application |
| ◆ | section break. `---` renders as a rule with a diamond |
| § | section anchor |
| ↗ | the link leaves the vault |

Sections in documents are numbered `01.`, `02.` and dates are written in ISO 8601 form (`2026-11-17`).

## 03. Writing with it

### Formal objects

The formal callouts are typeset like the amsthm package of LaTeX. Each one has a small label tab such as `THEOREM 03`, the name of the object in Garamond, and a violet rule at the left.

> [!definition] Formal object
> A **formal object** is a callout of the theorem family: a definition, a theorem, a lemma, a proposition, a corollary, a claim, a conjecture, an axiom, a remark, an exercise, or one of their relatives. All formal objects in one note share one counter.

| Type | Short alias | Look |
|---|---|---|
| `definition` | `def`, `defn` | double rule, tinted tab (stated, not proven) |
| `theorem`, `lemma`, `proposition`, `corollary` | `thm`, `lem`, `prop`, `cor` | double rule, filled tab (proven), italic body |
| `claim` | `clm` | tinted tab (stated) |
| `conjecture` | `conj` | dashed rule, hollow □ tab (open) |
| `axiom`, `postulate` | `ax`, `post` | tinted tab, like a definition |
| `remark`, `observation`, `notation` | `rmk` or `rem`, `obs`, `nota` | hairline rule, italic heading |
| `exercise`, `problem` | `exr`, `prob` | hollow □ tab, single rule |
| `proof`, `solution` | `pf`, `sol` | not numbered. Begins *Proof.* and ends with ∎ |

**Numbering.** The whole theorem family shares one counter in a note, as with `\newtheorem{lemma}[theorem]{Lemma}` in amsthm. Hypotheses (`H.01`), assumptions (`A.01`), equations (`(01)`), figures, tables and algorithms each have their own counter. Numbering is exact in Reading view and in PDF export. In Live Preview the editor renders only the lines near the screen, so numbers in a long note can be too low.

**Names and aliases.** CSS cannot distinguish a title that you typed from the default title that Obsidian supplies. The theme therefore uses a convention. The long type name shows its title as the name of the object. The short alias never shows a title. Use the alias for an object without a name.

**Modifiers** go after a `|` inside the brackets. You can combine them with spaces.

| Modifier | Effect |
|---|---|
| `star` or `nonum` | no number, and the counter does not advance (like `theorem*`) |
| `anon` | hide the title text and show only the label |
| `upright` / `italic` | change the body style of this one object |
| `titled` | show the title of an equation as a small tag |
| `left`, `nofloat`, `wide` | placement of an infobox or a table |

This source:

```markdown
> [!theorem] Monotone convergence
> Every bounded monotone sequence in $\mathbb R$ converges.

> [!pf]
> Let $(a_n)$ be increasing and bounded, and let $s=\sup_n a_n$.
> For $\varepsilon>0$ there is an $N$ with $a_N>s-\varepsilon$.
> Then $s-\varepsilon<a_n\le s$ for all $n\ge N$.

> [!theorem|star] Unnumbered result
> This theorem has a name and no number.

> [!thm|anon]
> This theorem has a number and no name.
```

renders as:

> [!theorem] Monotone convergence
> Every bounded monotone sequence in $\mathbb R$ converges.

> [!pf]
> Let $(a_n)$ be increasing and bounded, and let $s=\sup_n a_n$.
> For $\varepsilon>0$ there is an $N$ with $a_N>s-\varepsilon$.
> Then $s-\varepsilon<a_n\le s$ for all $n\ge N$.

> [!theorem|star] Unnumbered result
> This theorem has a name and no number.

> [!thm|anon]
> This theorem has a number and no name.

### Lab-paper callouts

| Use | Type (aliases) | Look |
|---|---|---|
| a testable hypothesis | `hypothesis` (`hyp`) | own counter `H.01`, amber dashed rule |
| a premise of a model | `assumption` (`asm`) | own counter `A.01`, solid steel rule |
| steps that someone can repeat | `experiment`, `method`, `procedure`, `protocol` | steel plate, numbered steps |
| a settled outcome | `result` (`finding`) | strong solid edge, filled ■ |
| a limit on a result | `caveat` | amber left rule, small italic text |
| raw numbers from a run | `measurement` (`readout`, `reading`, `lcd`) | display panel, mono figures |
| an equation that you cite later | `equation` (`eq`) | centred, numbered `(01)` at the right |
| an image with a caption | `figure` (`fig`) | `Fig. 01`, caption below |
| a data table with a caption | `table` (`tab`) | `Table 01`, caption above, three rules |
| pseudo-code | `algorithm` (`alg`) | `Algorithm 01`, numbered lines |

### Wiki callouts

| Use | Type (aliases) | Look |
|---|---|---|
| a pointer at the top of a section | `seealso`, `main`, `further` | one hatnote line: "See also:", "Main article:" |
| a short page that needs more text | `stub` | hatched |
| a claim that needs a source | `citation-needed` (`cn`) | a small mark at the right |
| a page that lists meanings of a term | `disambiguation` | dotted, a list of links |
| a section in progress | `wip` | amber, dashed, hatched |
| a reference list | `references` (`refs`, `bibliography`) | a `1.` list becomes `[01]`, `[02]` |
| one bibliographic entry | `cite` | dotted, hanging indent |
| facts beside the text | `infobox` | floats right in Reading view |
| links at the end of a page | `navbox` | centred box of links |
| abstract, key points | `abstract`, `summary` (`tldr`) | small-caps heading; ruled bar |

The standard Obsidian callouts (`note`, `info`, `tip`, `success`, `question`, `warning`, `failure`, `danger`, `bug`, `example`, `quote`, `todo`) are drawn as instrument plates: a thin border, a tinted title band and a condensed-caps label.

A callout is for a separate object that a reader will look for, cite or skip. It is not for emphasis. If the text reads correctly without the box, write it as a paragraph.

### Page types

A note can carry one `cssclasses` value. The theme then gives the page a small label above the title (the kicker) and a layout for its kind.

```yaml
---
tags:
  - type/article
  - status/draft
  - information-theory
cssclasses:
  - type-article
---
```

| cssclass | Page treatment |
|---|---|
| `type-article` | encyclopedia page with an ARTICLE kicker and ruled h2 headings |
| `type-person`, `type-group` | biography or organisation; the first paragraph is a lead |
| `type-paper` | reading notes: NOTES ON kicker, italic title, first quotation styled as the citation |
| `type-timeline` | list items become a dated timeline on a spine |
| `type-index` | lists flow in columns |
| `type-glossary` | a bold term at the start of a list item is set as a headword |
| `type-note` | working note with a quieter title |
| `type-memo` | memorandum with a running head and a cover-sheet look |
| `type-proof` | centred title; the page ends with ∎ |
| `type-project`, `type-event`, `type-dataset` | kicker; a dataset page has wider tables and mono numbers |

### Tags

Each tag answers one question, and its prefix says which question. The theme recognises the family from the prefix, so you need no list of tag names.

| Family | Question | Form | Colour |
|---|---|---|---|
| Topic | What is the note about? | no prefix: `information-theory`, `statistical-physics/spin-glass` | teal (blue in dark mode) |
| Type | What kind of document is it? | `type/…`, exactly one per note | blue-violet |
| Status | How finished is it? | `status/…`: `empty`, `stub`, `draft`, `review`, `stable`, and flags such as `rewrite` or `merge` | amber. `stable` is green; `empty` and `trash` are rose |
| Meta | Is it about the vault itself? | `meta/…` | slate gray |
| Author | Who wrote it? | `author/…` | copper |

All tags have the same shape, border, weight and contrast. The families differ only by hue, and the hues have matched lightness, so no family looks louder than another. A value such as a date, a source or a revision number is a property, not a tag.

**Tag styles.** There are six, chosen in Style Settings. **Plectics**, the default, is the theme's own look. **Path** splits a tag at its first "/": `#type/article` shows `type` plain and `/article` shaded in the family colour, because the leaf is the information and the prefix is only the filing. **Obsidian, coloured** keeps Obsidian's pill shape, filled with a light tint of the family colour. **Obsidian, half** is the same with the part before the "/" filled solidly. **Label** and **Plain** are quieter. The two styles that split a tag need the Typed Notes plugin; without it a tag is drawn whole.

**Tags in the Properties box.** Obsidian gives these chips no per-tag hook, so the theme cannot see their family on its own. The Typed Notes plugin marks each chip, and the chips then take the family colours too. You can also define up to three tag groups of your own in the plugin and give them colours in Style Settings.

## 04. Options

All options are in one Style Settings section, **Plectics Alto**, in seven groups: Text, Interface, Dark mode, Icons and file list, Notes and properties, Typed tags, Canvas. The theme works without the plugin; every option is a body class or a CSS variable with a default, and every default looks the same with or without Style Settings. The full list is in [SETTINGS.md](SETTINGS.md).

**Fonts.** Three faces are built in: Alto Garamond Condensed (titles; EB Garamond condensed to 80 % with re-weighted stems), Archivo (interface) and Nimbus Sans (caps labels). The reading face is Constantia, with options for CMU Serif (matches LaTeX maths), IBM Plex, EB Garamond and others if installed.

**Chicago.** The classic Macintosh used Chicago for window titles, menus, alerts and buttons, and never for document text. The theme does the same if the free ChicagoFLF font is installed. "Titles and alerts" covers dialog titles, the window title, notices and canvas group labels. "Titles, menus and buttons" adds menus, buttons, tabs and tooltips. Reading text, code and numbers never use Chicago.

**Controls.** Buttons, toggles, sliders, dropdowns and progress bars are one family, drawn from one size scale (16, 20, 22, 24 and 28 px) and one bevel style.

**Icons.** Plectics Alto draws Lucide line icons for file types and folders. **Plectics Alto Icons** draws the hand-drawn Farm-Fresh 16 px colour icons instead (32 px on HiDPI screens), embedded in its CSS. If the Iconize plugin has set an icon on a row, an option decides which icon is shown.

## 05. Plugins

**Recommended**
- **Typed Notes** ([obsidian.plugin.typed-notes](https://github.com/1800MIRACLE/obsidian.plugin.typed-notes)): marks each tag with its family, for the coloured Properties chips and the styles that split a tag. It also shows a note's `title` property as the note's title. This completes the look.
- **Style Settings**: shows the options of §04. Optional; every default holds without it.

**For mathematics**
- **Latex Suite**: fast entry of LaTeX with snippets and shortcuts.
- **LaTeX-like Theorem & Equation Referencer** (formerly Math Booster): theorem and equation environments with numbering you can link to. The theme's own callout numbers are visual only. Use one numbering, not both.

**For references and tidy notes**
- **Citations** or **Zotero Integration**: literature notes from a bibliography; a template can emit the theme's `references` and `cite` callouts.
- **Linter**: keeps tags in the `tags` property, where Typed Notes can colour them.

**For Canvas**
- **Advanced Canvas**: dashed and dotted edges, arrow styles and collapsible groups, all drawn by the theme.

The theme also styles many other community plugins (Kanban, Calendar, Dataview, Tasks, Templater, Excalidraw, Homepage, Git and more) and the core Canvas, Bases and Graph views. See [DEPENDENCIES.md](DEPENDENCIES.md).
