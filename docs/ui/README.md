# Dave’s & Enemies — UI handoff

Prepared against Claude’s `docs/PROJECT_CONTRACT.md` and `docs/ASSET_REQUESTS.md`, plus the original game brief. Design reference: **1280 × 720 GUI**. GameMaker integration remains with Claude.

Start with [UI_SPEC.md](UI_SPEC.md). It contains exact rectangles/anchors, spacing, fonts, colors, state styling, keyboard/mouse navigation, inventory rules, dialogue/hotbar routing, save confirmations, scaling, and terminal screens.

| Deliverable | File |
|---|---|
| Overview of all 14 layouts | [UI_OVERVIEW.png](UI_OVERVIEW.png) |
| Annotated native inventory layout | [03_inventory_annotated.png](mockups/03_inventory_annotated.png) |
| Annotated speaker dialogue layout | [06_dialogue_pharaoh_annotated.png](mockups/06_dialogue_pharaoh_annotated.png) |
| Complete screen references | `mockups/01_…` through `14_…`: native PNG, editable SVG, annotated PNG |
| Implementation specification | [UI_SPEC.md](UI_SPEC.md) |
| Rectangles, colors, typography, repetition formulas | [UI_LAYOUTS.json](UI_LAYOUTS.json) — design data, not a replacement runtime schema |
| Panel/icon/border/portrait manifest | [UI_ASSETS.csv](UI_ASSETS.csv) |
| Engine acceptance checklist | [UI_QA_CHECKLIST.md](UI_QA_CHECKLIST.md) |
| Static verification evidence | [QA_REPORT.json](QA_REPORT.json) |
| Source asset IDs and font metadata | `assets/`, `fonts/FONT_INFO.json` |
| Rebuildable drawing sources | `source/render_ui.py`, optional `source/prepare_fonts.py` |

Normal gameplay has health and eight main slots only. Inventory shows 32 additional slots, current equipment, item descriptions, level, and XP; the eight main slots stay visible in inventory mode. Dialogue hides the main row and disables its input. Combat pauses for both views. All textual UI remains editable in GameMaker.

The mockup scene, portraits, and item illustrations are **schematic placeholders**. They establish placement and contrast, not final art direction or completed production art. The manifest preserves requested IDs such as `spr_portrait_dave`, `spr_portrait_pharaoh`, and `spr_icon_potion_health` and marks them as outstanding art requests. The UI package supplies a **text-free prototype frame kit** using the contracted IDs/dimensions, plus Noto Sans Regular/Bold static TTFs and the OFL licence. No GameMaker object, script, sprite resource, room, or project configuration was modified.

Prototype sprite delivery: PNG, RGBA 8-bit, straight alpha, sRGB chunk. Frame `_00` = normal, `_01` = hover, `_02` = pressed. For multi-state assets import the numbered frames into the base asset ID listed in the manifest; suffixes are delivery frame names, not new resource IDs. All UI source origins are top-left. Panel nine-slice borders = 24 px, buttons = 16 px, HP caps = 8 px. Counts, names, portraits, and icons are drawn separately. UI color/state rendering remains in Claude’s controller code.

The font instances were produced from the official [Google Fonts Noto Sans source](https://github.com/google/fonts/tree/main/ofl/notosans), at width 100 and weights 400/700. `fonts/OFL.txt` must accompany font distribution. `fonts/FONT_INFO.json` records instance hashes, style names, and coverage for the contract’s character set. Use supplied static TTFs rather than relying on a user’s installed system font.

Rebuild PNG/SVG references and static checks from the project folder:

```powershell
python docs/ui/source/render_ui.py
```

This requires Python and Pillow. The optional font rebuild uses fontTools and the already supplied variable font; it makes no network requests:

```powershell
python docs/ui/source/prepare_fonts.py
```

Static checks passed at delivery: **14 native layouts, 93 safe-area rectangles, 113 measured text fits, 14 RGBA/sRGB prototype image sources**. Sample text contrast ranges from **5.23:1** (disabled on raised) to 15.5:1. The widest-letter 140-character dialogue case paginates safely rather than overflowing two lines. Scaling examples include 1920 × 1080 inventory and 3440 × 1440 pillarboxed gameplay.

These checks do not validate GameMaker compilation, save I/O, state routing, real input, or gameplay. Claude should implement the package and complete the unchecked engine acceptance list in the IDE. Keep existing working resources until replacements pass contract validation.
