# Dave’s & Enemies — UI_SPEC

Design handoff · 31 October 2026 · reference canvas **1280 × 720**

Claude owns implementation and integration. This package supplies visual layouts, tokens, asset specifications, fonts, and acceptance criteria. The PNGs are review images; draw every label, number, item description, key prompt, and dialogue string as editable text in GameMaker.

## 1. Sources and contract alignment

Read against `../PROJECT_CONTRACT.md` §§1–2, 8–11 and `../ASSET_REQUESTS.md` A9–A12, B9, D1, E5, F8, as available on 31 October 2026. The original brief was recovered from the chat **Create Dave’s action game prompt**, including the original user message and its expanded development prompt. Preserve the story, exactly eight hotbar slots plus 32 additional storage slots, three save slots, and the pre-boss exchange.

| Contract requirement | Design decision |
|---|---|
| GUI 1280 × 720 [P]; camera 1280 × 720 [V] | All coordinates below are logical GUI pixels, independent of room/camera coordinates. Adopt the contract’s GUI proposal. |
| Smooth cartoon art, dark outlines, top-left light, filtering on | Dark ink panels, warm ivory text, restrained gold edges, softly rounded corners. No pixel font or pixel-grid ornament. |
| Slots 72 × 72; icons 64 × 64, readable at 48 | Render item icons at **48 × 48** inside unchanged 72 px slots. |
| Portrait source 512 × 512, facing right, drawn 208 × 208 | Both speakers use the same **208 × 208** left-hand portrait position. |
| One OFL family, 23 / 28 / 46 px, minimum 18 | Noto Sans Regular + Bold; supplied with OFL licence. Four sizes: 18, 23, 28, 46. |
| `spr_ui_hp_frame`, `spr_ui_hp_fill`, `spr_ui_slot`, `spr_ui_slot_selected`, `spr_ui_panel`, `spr_ui_save_card`, `spr_ui_save_card_empty`, `spr_ui_button` | Preserve these exact asset IDs and their requested source sizes. Destination rectangles can differ from source sizes using specified nine-slice borders. |
| Speakers `dave`, `pharaoh`, `narrator`; items snake_case | Use `spr_portrait_dave`, `spr_portrait_pharaoh`, `spr_icon_<item_id>`. No alternative item or speaker identifiers. |
| Dialogue entries ≤140 characters; two lines at 28 px | Measure actual wrapped text; paginate an entry when it exceeds two lines. Character count alone cannot guarantee fit. |
| Windows VM, 60 fps; IDE play-testing required | Use time in milliseconds for presentation; pause world simulation independently of GUI/input. No compile or gameplay validation is claimed here. |

The contract does not name UI controller objects, save-file fields, UI action enums, font resources, or equipped-item reference fields. Names prefixed `ui.` in this package are **design keys**, not new GML globals or required runtime names. Proposed `fnt_ui_*` resource aliases are additions for Claude to map to his implementation; close, focus, equipped, and empty-state indicators can be drawn in code without introducing extra sprite IDs. Do not rename existing resources or change save schemas to match this document. Numeric sample HP, XP, equipment, save dates, and playtime in mockups are illustrative.

## 2. Visual tokens and typography

| Token | sRGB hex | Use |
|---|---|---|
| ink | `#171B27` | Opaque panel and button background |
| raised | `#242A39` | Hover, selected-row background |
| well | `#101521` | Empty slots, bar tracks |
| edge | `#747F95` | Ordinary control outlines |
| gold | `#EAC477` | Selected, focus, primary accents |
| text | `#F6EBDD` | Primary text |
| muted | `#B9C3D3` | Secondary text |
| disabled | `#929DAF` | Disabled labels, with lock/dash and reason |
| health | `#C14F5C` | Dave HP fill |
| boss | `#A663C1` | Pharaoh HP fill |
| xp | `#6FB8C9` | Inventory XP fill |
| error | `#FFAC9F` | Errors and destructive outline/text |
| success | `#A5D6A0` | Save success, positive comparison |

Text/muted/disabled on opaque ink are intended to exceed 4.5:1; gold focus against ink exceeds 3:1. See generated `QA_REPORT.json` for measured pairs. Do not place body text directly over sand or translucent art. HP and XP use numbers as well as length; selection uses an outline plus marker, so color is never the sole cue.

Panel: opaque ink, 2 px edge, 12 px radius, 1 px inset highlight at the top. Use gold only for focus and small corner accents. Source `spr_ui_panel` 96 × 96, nine-slice **24 px** on every side. Content padding 24 px; inter-section spacing 24–40 px. Button source 64 × 64 with **16 px** borders; final button height 48 px normally. Quiet small actions may be 40 px high. Do not include button text in the source art. No noisy parchment behind text, decorative script, or extra HUD meters.

| Design alias (proposed resource) | Family / weight | Pixel em | Line box | Use |
|---|---|---:|---:|---|
| `ui.type.meta` / `fnt_ui_meta` | Noto Sans Regular | 18 | 24 | Keycaps, counts, dates, secondary stats, captions |
| `ui.type.body` / `fnt_ui_body` | Noto Sans Regular | 23 | 30 | Buttons, values, descriptions, ordinary UI |
| `ui.type.heading` / `fnt_ui_heading` | Noto Sans Bold | 28 | 36 | Panel headings, dialogue speaker name |
| `ui.type.dialogue` / `fnt_ui_dialogue` | Noto Sans Regular | 28 | 36 | Dialogue body |
| `ui.type.title` / `fnt_ui_title` | Noto Sans Bold | 46 | 58 | Pause, Save/Load, Settings, Game Over, ending |

Sizes are **rendered GUI pixel ems**, not assumed GameMaker editor point sizes. Use the supplied static Regular/Bold files at the specified pixel size, or build font assets whose measured output matches them. Never scale an 18 px font to simulate 23 px. Measure with the final font; support ASCII plus `— … ’ “ ” ×`. Use ASCII key names and words for unavailable symbols (`Left/Right`, `Level`, `HP`, `XP`). No smaller text for long names: wrap or ellipsize instead. Preserve case from item data; menu labels use sentence case. Use tabular-looking right-aligned numeric fields without adding another family.

## 3. Coordinate, rendering, and scaling rules

Rectangles are `(x, y, width, height)`, top-left origin. Edges are half-open for hit-testing: `x <= mx < x+w`, `y <= my < y+h`. Text coordinates below are the **top of a line box**, not a font baseline. Center/right alignment is explicit. Source sprite origins for UI assets are `(0,0)`; portrait/item sources also use `(0,0)` because destination rectangles determine placement. World sprite feet origins stay as specified by Claude.

The GUI content plane remains 1280 × 720. Safe outer margin = **24 px**. Use the same transform for art, text, focus outlines, clipping rectangles, and pointer coordinates. Keep camera shake and world zoom out of the GUI transform.

For an available client area `W × H`, use `s = min(W/1280, H/720)`, content size `1280s × 720s`, centered offsets `(W-1280s)/2`, `(H-720s)/2`. Draw black letterbox/pillarbox bars outside this content rectangle. **Do not independently stretch axes.** Preserve the application’s existing aspect handling if it already provides the same result. Fixed GUI size alone does not guarantee aspect preservation: configure/composite the GUI with the content viewport. If engineering uses an explicitly composited UI surface, use that surface’s exact transform once, not an additional GUI scale on top.

Convert pointer coordinates through that same transform; reject events outside the content rectangle. When GameMaker’s GUI transform already matches the plane, use its GUI-coordinate mouse functions. For a custom content surface use `gui_x=(client_x-offset_x)/s`, `gui_y=(client_y-offset_y)/s` instead; never perform both conversions. At 1600 × 900, `s=1.25`; 1920 × 1080, `s=1.5`; 2560 × 1440, `s=2`; 3440 × 1440, content 2560 × 1440 with 440 px side bars; 1280 × 800, content 1280 × 720 with 40 px top/bottom bars.

The 1280 × 720 layout is the minimum supported readable client content size. In windowed mode use this minimum if resizing is supported; current template resizing is off. Smaller displays may proportionally fit the canvas as a fallback, but are outside the readability acceptance target (18 px becomes 13.5 px at 960 × 540). Scaling magnifies the composition; it does not require larger source artwork. Use anti-aliasing and filtering per contract. Snap coordinates consistently; do not round fill ratios until calculating the final GUI fill width. Re-render fonts at physical target resolution if a blurred surface-text pass is observed; keep logical layout unchanged.

Suggested drawing order, back to front: world → world weather → health/boss/hotbar → modal dim → inventory/dialogue/pause/save → nested confirmation → active focus/cursor. Draw state exclusivity below determines which layers exist. Draw transition whiteout last; it also blocks input. Reset draw alpha, color, font, alignment, and clip state after each component.

## 4. Gameplay, boss health, and the hotbar

See `01_gameplay`, `02_boss` and `13_component_states` in `mockups/` (PNG and editable SVG).

| Element / design key | Rectangle or text placement | Detail |
|---|---|---|
| `ui.hp` | Group `(24,24,320,56)` | Only permanent top-left component. |
| HP label / value | `(32,24)` 18 px; value right-aligned `(336,24)` | `HP` and `104 / 140`; opaque ink backing `(24,24,320,56)` keeps labels readable over any world terrain. |
| HP source frame | `(24,48,320,32)` | Preserve A10 source size. Optional nine-slice caps 8 px. |
| HP track/fill | `(32,56,304,16)` | Fill width `304*clamp(hp/max_hp,0,1)`, clip inside track; 0 width at zero. |
| `ui.hotbar` | `(324,624,632,72)` | Bottom center: `x=(1280-632)/2`, `y=720-24-72`. Eight slots only; no extra bag button. |
| Hotbar slot `i` | `(324+80*i,624,72,72)`, `i=0…7` | 8 px gap. Slot visuals and hit areas are identical. |
| Slot icon | local `(12,8,48,48)` | Contract 64 px source downsampled to 48. No icon in an empty slot. |
| Key label | local `(6,2)` 18 px | `1…8`, dark backing 20 × 24 when overlapping an icon. |
| Stack quantity | right-aligned local `(64,48)` 18 px | Draw only if quantity >1, e.g. `×9`; dark backing when needed. Never invent a count for an unstackable weapon. |
| Active slot | 2 px gold border inset 1, 4 px corner ticks | A short 20 × 3 gold bottom marker distinguishes active from hover. |
| `ui.boss` | `(384,24,512,64)` | Appears only during active Pharaoh encounter. HP group and hotbar remain. |
| Boss name | centered `(640,24)` 23 px | `The Undead Pharaoh`, one line. |
| Boss frame / fill | `(384,56,512,32)` / `(392,64,496,16)` | Reuse HP frame/fill, tint fill boss purple. Stretch frame center, preserve 8 px caps. No phase counter or permanent extra HUD. |

The ordinary HUD contains **only HP and eight main slots**. No permanent XP, level, coins, minimap, quest tracker, equipment strip, or inventory capacity. Checkpoint prompts and failed-action feedback are temporary, not HUD widgets. Failed action text uses `(384,568,512,40)`, opaque ink, 18 px, centered; at most one message, shown for 1800 ms; a repeated event extends it but does not stack it. Example: `Inventory full. Loot remains here.` Show only after an actual failed pickup; leave the loot/chest reward available.

Gameplay controls: `1–8` selects the corresponding main slot; wheel up/down cycles main slots once per detent, including empty slots, with wrap. Left-click on a main slot selects it and consumes the click; left-click elsewhere performs Claude’s world attack. `Q` uses the selected consumable only; full HP or unusable/empty selection consumes nothing and shows a short reason. Weapon and armor equipping occurs in inventory, not as an accidental result of selecting a main slot. `I` or `Tab` opens inventory; right-click any main slot is the mouse route and opens inventory focused on that slot. A temporary hover hint after 500 ms can say `Right-click: inventory`; remove it on pointer exit. No persistent ninth control.

Damage may show a delayed pale fill behind the true HP for 250 ms; the true fill updates immediately. Low HP ≤25% adds a static pale notch at the left and high-contrast numeric text; do not pulse the whole screen. Boss damage uses the same behavior. During the defeat sequence, hold zero HP briefly, then hide boss UI at the whiteout; do not return a living boss bar on fade-in.

## 5. Expanded inventory, equipment, and item descriptions

See `03_inventory` and `04_inventory_full`. Pause all world simulation, enemy projectiles, damage, attack animation timers, weather spawning, and playtime while inventory is open. GUI feedback continues. Draw a 45% ink dim over the world, suppress the top health and boss bars, keep the eight main slots visible at their **unchanged gameplay coordinates**. Their mode becomes inventory selection/movement, not combat selection/use. The inventory is one modal view containing the 32-slot panel and the main row.

| Element | Rectangle / text | Detail |
|---|---|---|
| Main panel | `(56,40,1168,560)` | Nine-slice `spr_ui_panel`, 24 px content padding. |
| Heading | `(80,64)` 28 Bold | `Inventory` |
| Close | `(1160,56,40,40)` | Editable `X`; mouse close. Hit area 40 × 40. |
| Storage heading / capacity | `(80,116)` 23; right `(712,116)` 18 | `Storage`, `13 / 32`; capacity counts **storage only**. |
| Storage grid | `(80,152,632,312)` | **8 columns × 4 rows = 32** extra slots; 72 px square, 8 px gaps. |
| Storage cell `(c,r)` | `(80+80*c,152+80*r,72,72)` | `c=0…7, r=0…3`; logical item index `8+8*r+c`. |
| Character / level | `(752,64)` 23 | `Dave / Level 6`; no character portrait needed. |
| XP track / fill | `(752,104,376,16)` | Cyan proportional fill, cap at track. |
| XP text | `(752,128)` 18 | `XP 240 / 400`; at cap show `Maximum level`, hide denominator. |
| Weapon summary | `(752,160,216,96)` | Label, 48 px icon, fitted name, current damage stat. |
| Armor summary | `(984,160,216,96)` | Label, icon, fitted name, current defense stat. |
| Item detail panel | `(752,280,448,296)` | Same opaque well; 24 px inset. |
| Item name | `(776,304,400,60)` 23 | Up to 2 lines; no abbreviation of actual data. |
| Item type / stat comparison | `(776,368,400,24)` 18 | Text such as `Consumable / Restores 30 HP` or `Damage 6 → 8` using `6 to 8` for glyph safety. Compare actual resulting totals, not guessed stats. |
| Description viewport | `(776,400,400,114)` | 23 px, 30 px line step; clip and scroll if more than 3 lines. Wheel while over pane; PageUp/PageDown when pane focused. Add a small scroll indicator if overflow exists. |
| Primary / Move buttons | `(776,528,192,40)` / `(984,528,192,40)` | Primary label depends on item: `Use`, `Equip`, `Equipped`, or `No action`. |
| Status line | `(80,492,632,60)` 23 | Up to 2 lines; full/incompatible/success feedback. Reserve this space even when blank. |
| Keyboard hints | `(80,556)` 18 | `Enter Action   M Move   F6 Area   I / Tab Close` |

**Storage model:** the hotbar owns storage entries 0–7 and the grid owns 8–39. Equipment summaries reference entries already among these 40; they do not grant two extra storage slots or duplicate items. Moving an equipped item keeps its equipped reference valid. Replacing equipment changes a reference after validating the new item. Claude may retain his equivalent storage model, provided capacity remains exactly 40 and swaps cannot duplicate items. No third equipment category is invented.

**Inspect and use:** left-click selects a slot and updates the right pane; clicking does not consume or equip. Enter invokes the selected item’s primary action. Double-click is not required and has no extra semantics. Using a potion decrements one only after a successful heal. At full HP, `Use` is disabled and description says `Health is already full.` Equipped items show a small `E` badge and the disabled primary label `Equipped`. Empty selected slot shows `Empty slot`, `Move an item here.`, and disabled primary/Move controls. Valuables have `No action`, disabled, with explanatory text. Do not imply selling, dropping, or discarding systems not present in this chapter.

**Move:** `M` or the Move button picks up the whole selected stack into a move preview; a left-click on a different slot or Enter places it. Pointer movement is optional; keyboard arrows provide the same operation. Source is not deleted until commit. Same-item stacks merge up to the item’s actual `stack` limit (potion_health example: 9); remainder stays at source. Unlike items swap atomically. An empty target receives the whole stack. Moving onto source cancels. `Esc` / right-click cancels move before closing inventory. Closing while carrying cancels and returns the item to its original source, with no world drop. No stack-split feature is required. Show source dashed outline, target gold corners, and a 48 px icon ghost with count; invalid target gets error outline and a reason, not a red-only signal.

**Keyboard focus:** arrows navigate the storage grid spatially; bottom-row Down enters the main row in the same column, and main-row Up returns to storage row 4 in that column. Clamp other edges; no wrapping. `1–8` focuses a main slot without activating it. `F6` cycles storage → main row → weapon/armor summaries → description → action buttons → Close; Shift+F6 reverses. Arrows change controls within a zone; Enter activates a focused button; Space is also allowed on buttons. `Tab` and `I` close the inventory to preserve the brief’s toggle controls, so they are not focus traversal here. Escape first cancels an active move, otherwise closes. Remember the previously focused slot for the next open. On first open focus main slot 1, or the slot right-clicked.

**Full capacity:** an inventory is full when all 40 entries are occupied and no compatible stack has capacity for the incoming quantity. Check the combined storage model, not just the 32-grid count. A partially mergeable pickup takes only what fits if Claude supports partial pickup and leaves the exact remainder; otherwise reject the whole pickup. Never silently destroy the remainder. Error text: `Inventory full. Loot remains here.` Mark capacity in error color and with the word `Full`; retain all slot focus and selection. Full capacity never blocks rearranging, equipping, consuming, or closing.

## 6. Dialogue and encounter handoff

See `05_dialogue_dave`, `06_dialogue_pharaoh`. Dialogue replaces the bottom hotbar completely; hidden slots have **no hitboxes, tooltips, wheel selection, number shortcuts, or Q use**. Inventory cannot open during dialogue and is not queued to open afterward. World attacks and movement are blocked. Health may remain at top-left; boss bar is absent during the introduction. Combat starts after the final line, never under the dialogue.

| Element | Rectangle / placement |
|---|---|
| Dialogue panel | `(24,440,1232,256)` |
| Portrait | `(48,464,208,208)`; draw contract 512 px source facing right |
| Portrait edge | 2 px inset frame, never crops face; source has 16 px safe padding |
| Speaker | `(280,464)` 28 Bold; `Dave` or `The Undead Pharaoh` |
| Text viewport | `(280,512,928,80)`; 28 Regular, 36 px line step, at most 2 lines per page |
| Advance hint | `(280,648)` 18; `Enter / Space / LMB  Reveal` while typing, then `… Continue` |
| Page marker, if needed | right `(1208,648)` 18; `1 / 2` |

Use the contract’s `boss_intro` lines exactly: `dave`: **Step aside.** `pharaoh`: **You shall not pass. This desert will be your grave.** Resolve portrait from speaker ID. `narrator` uses no portrait or fake speaker name; reclaim portrait space with text at `(48,496,1160,108)` and preserve the footer.

Reveal at 30 characters/second as a presentation default, with 120 ms comma/semicolon and 220 ms sentence-end pause. One fresh Enter, Space, or left-click reveals the current page and stops pending blips; the next fresh activation advances. An input can never reveal and advance in the same event. Ignore a held attack that opened the scene. No automatic timeout. There is no dialogue-choice UI in this chapter.

Escape opens a pause overlay above the dialogue and freezes text reveal; Resume restores the current page. Settings may be reached through this pause overlay. A separate `Skip scene` action may be shown only in this dialogue-origin pause: its confirmation uses the standard modal, and accepting must call Claude’s scene-completion path that closes the gate, sets the one-shot intro flag, clears intro hazards, starts the theme, shows boss HP, and enables combat in the correct order. Do not simulate skipping by simply deleting the panel. The same gate/state initialization applies after reading the final line. Require all activation controls to be released before handing control back to combat.

## 7. Three-slot Save/Load and confirmations

See `07_save`, `08_load`, `09_overwrite`. Save is available from an in-world star checkpoint, not from ordinary combat. Pause may show a disabled Save Game action with `Save at a checkpoint.` Main-menu load and Game Over load use the same layout. No fourth or auto-save slot appears.

| Element | Rectangle / text |
|---|---|
| Panel | `(208,72,864,600)` |
| Heading | `(232,96)` 46 Bold, `Save Game` or `Load Game` |
| Save / Load mode tabs | `(752,112,132,36)` / `(896,112,132,36)`; 18 px, optional if only one mode available; active mode has a bottom marker, keyboard focus has corner ticks |
| Slot `n`, 0-based | `(260,192+128*n,760,120)`; exactly 3 rows, 8 px gaps |
| Row number | `(284,row_y+18)` 28 Bold, `1`, `2`, `3` |
| Location / empty label | `(332,row_y+16,664,30)` 23 |
| Metadata | `(332,row_y+56,664,24)` 18 |
| Secondary row status | `(332,row_y+88)` 18; `Selected`, `Empty`, `Cannot load`, or blank |
| Footer status | `(232,584,632,24)` 18 |
| Back / primary | `(232,608,160,40)` / `(888,608,160,40)` |

The final row ends at 568. Footer status begins at 584; buttons end at 648, leaving 24 px to the panel’s lower edge at 672.

Each occupied row displays checkpoint/location name, level, `HH:MM:SS` playtime, and saved local date/time (example `31 Oct 2026 13:05`). These are display fields read from Claude’s save metadata, not a new save schema. Long location names ellipsize to the available width; the full name appears in the footer on focus. Metadata never overlaps the slot number. Do not show a thumbnail requirement or a delete-save feature.

Save mode: empty and occupied rows are selectable. Default to the active save slot if present, else first empty, else slot 1. Enter/click selects a row; only the bottom primary `Save` commits intent. An occupied slot opens overwrite confirmation. An empty slot writes without overwrite confirmation. Do not make double-click write. Save restores health only after a successful checkpoint transaction. Show `Saving…` and disable Back, tabs, slot activation, and primary while the write is in flight. On success say `Saved to slot 1. Health restored.` and keep the screen open. On failure keep the previous save intact and say `Save failed. Your previous save is unchanged. Try again.` only if engineering can guarantee that; otherwise report the actual failure without promising recovery.

Load mode: empty rows are visibly marked `Empty slot` / `No saved journey` and cannot load. Invalid/corrupt/incompatible rows show `Cannot load this save` and a specific reason in the footer; preserve the file. Keyboard focus skips unusable rows, but hover can expose the reason. When all rows are unusable, focus Back, disable Load, and show `No saves available.` Occupied valid row selection enables `Load`. Loading from a running/paused session asks `Load slot 1? Unsaved progress will be lost.` Loading from main menu or Game Over needs no unsaved-session confirmation. While loading, lock controls and show `Loading…`; on failure return to the same row with a readable message.

Navigation: Up/Down changes row focus and selection together without wrapping; Left/Right switches available mode tabs only when tabs are focused. Tab / Shift+Tab cycles tabs → usable rows → Back → primary. Enter on a row selects without saving/loading, Enter on primary acts; Space activates buttons. Escape returns to the calling screen. Right-click also returns when not busy. Save mode tab is disabled outside a checkpoint; show reason on focus/hover. Returning restores the caller’s prior focus and paused state.

**Nested confirmation:** `(384,216,512,288)`, full-screen 60% ink scrim over the already open menu. Heading `(408,240)` 28 Bold; two-line message `(408,288,464,72)` 23; save date at `(408,376)` 18. Buttons: Cancel `(408,432,216,48)`, Overwrite `(648,432,224,48)`. Focus **Cancel** initially. Left/Right, Tab/Shift+Tab changes choice; Enter or Space activates. Escape/right-click cancels; outside-click does nothing. Require a fresh release/press after opening so the initiating Enter cannot confirm. Overwrite has error outline and explicit `Overwrite` text, no generic `OK`. Reuse this geometry for load/return-to-menu/quit confirmations with action-specific text. Cancel restores the exact row and button focus. Busy write/load cannot be cancelled halfway.

## 8. Pause and settings

See `10_pause` and `11_settings`. Freeze simulation, damage, world animation timers, and playtime. Keep the world dimmed beneath an opaque menu. Hide HUD and hotbar while paused; if invoked over dialogue keep the frozen dialogue beneath the dim. Save/load/settings are children of pause; Back always returns to their caller rather than unexpectedly resuming combat.

Pause panel `(440,88,400,544)`. Heading `(464,112)` 46 Bold. Six buttons `(464,200+60*n,352,48)`: Resume, Settings, Save Game, Load Game, Main Menu, Quit Game. Footer `(464,580,352,24)` 18. Save Game is disabled outside checkpoint context; Load Game is disabled only if no valid slots. If paused over dialogue, replace disabled Save Game with `Skip scene` (only when skip is supported); load can be disabled during non-restorable cutscenes with a reason. These are context-specific labels for the same row, not extra controls. Main Menu and Quit Game require confirmation if the session has unsaved progress. Resume is initially focused and Escape resumes. Escape in a child first returns to pause. Never let Escape in Settings also resume the game in the same frame.

Settings panel `(208,72,864,600)`. Heading `(232,96)` 46 Bold. Rows `(232,188+64*n,816,48)`, six in order: Music, Sound effects, Dialogue blips, Reduced flash, Screen shake, Window mode. Label width 280. Slider tracks `(536,row_y+14,352,20)` with 24 px thumb; percent right-aligned at `(1048,row_y+8)` 23. Toggles/choice controls `(536,row_y,352,48)`. Back `(888,608,160,40)`; hint `(232,608)` 18. Focus first row on entry. Up/Down/Tab moves rows; Left/Right changes a volume by 5 percentage points (Shift = 1) or a discrete option. Home/End sets 0/100 for sliders; mouse click/drag adjusts continuously and captures pointer until release. Enter/Space toggles boolean controls. Do not capture world mouse while adjusting. Defaults are proposals: Music 70%, SFX 80%, dialogue blips 65%, Reduced flash off, Screen shake on, Windowed. Prefer established settings when they exist; never reset existing preferences on opening.

Settings persist immediately through Claude’s settings path, independently of a gameplay save. Reduced flash replaces the whiteout peak with a slow dark fade while preserving the boss-cleanup state sequence; no repeated flashes. Screen shake off removes camera shake without hiding attack telegraphs. Window mode changes between aspect-correct Windowed (1280 × 720 content) and Fullscreen if supported by engineering; if unsupported, disable the control and explain `Window mode is fixed in this build.` No unsupported resolution list or key-rebinding screen is implied. A disabled control stays legible, includes a dash/lock cue, accepts no activation, and offers a reason on focus or hover. Menus use both mouse and keyboard with the same states.

## 9. Game Over and chapter ending

See `12_game_over`, `14_to_be_continued`.

Game Over suppresses all HUD and world input and keeps the world stopped. Apply an 88% ink dim. Center title `(640,152)` 46 Bold, `Game Over`; subtitle `(640,220)` 23; checkpoint info `(640,268)` 18. Three buttons `(384,328+72*n,512,56)`: `Return to Last Checkpoint`, `Load Game`, `Main Menu`. Select the first usable button after a 600 ms settle and after activation controls are released. Restoring a checkpoint loads the saved snapshot, including inventory and world state; it is not a heal-in-place. If no checkpoint snapshot exists, first label becomes **Restart Chapter**, using Claude’s safe initial state. Load is disabled when no valid saves. Up/Down/Tab navigates; Enter/Space/left-click activates. Escape focuses Main Menu but does not activate it. Death does not trigger a save or overwrite a slot. Clear all old modal/move/attack states before restoration. Main Menu returns to the existing `rm_menu` path.

Ending uses existing `rm_ending` / `spr_ending_bg` IDs, drawn at 1280 × 720. Show an understated arch silhouette, no recovered Grail. Header centered `(640,168)` 18 `CHAPTER I`; title `(640,216)` 46 Bold **To Be Continued**; subtitle centered `(640,296)` 23 `Beyond the desert, the search goes on.` One button `(448,432,384,56)` `Main Menu`; small note centered `(640,520)` 18 `Your journey continues in the next chapter.` Fade in over 800 ms, then focus the button after controls are released. Enter/Space/left-click or Escape returns to main menu only after this settle period. This screen does not imply a new save: do not say `Progress saved` unless engineering has actually completed a checkpoint write. The chapter does not enter the dungeon interior.

## 10. Common state and input rules

| State | Health | Main slots | Boss bar | World simulation | Input owner |
|---|---|---|---|---|---|
| Exploration | visible | visible, combat selection | absent | running | gameplay, except consumed UI hit areas |
| Boss combat | visible | visible, combat selection | visible | running | gameplay, except consumed UI hit areas |
| Inventory | hidden | visible, inventory mode | hidden | stopped | inventory only |
| Dialogue | visible | hidden, no hit areas | absent for intro | stopped | dialogue only |
| Pause / Settings / Save / Load | hidden | hidden | hidden | stopped | top menu only |
| Confirmation | caller drawn beneath dim | caller beneath dim | caller beneath dim | stopped | confirmation only |
| Boss defeat / whiteout | sequence-dependent, then hidden | hidden | zero then hidden | engine-controlled cinematic; no damage | transition only |
| Game Over / Ending | hidden | hidden | hidden | stopped | that screen only |

Priority: busy transaction / transition → confirmation → child menu → pause → dialogue → inventory → gameplay. Do not run multiple screen handlers for one event. Inventory and dialogue are mutually exclusive; a dialogue trigger should wait until inventory closes if the engine can trigger a scene while a menu is open. Never steal an in-progress inventory move to start a scene. Death/ending forcibly cancel move previews through a no-loss cleanup path.

All actions use a fresh press unless explicitly holding a slider/scroll key. On any open/close/resume/scene-end, consume the triggering event and suppress gameplay actions until the relevant controls have been released. A held left mouse button over a menu must not start a sword swing when it closes. Q, E, number keys, wheel, and WASD are gated by mode; inventory arrows cannot move Dave. Tooltips and scroll regions do not receive input when their parent is hidden. Mouse hover changes hover only; keyboard focus does not jump until the mouse moves at least 3 GUI pixels or clicks. A click grants mouse focus. Do not process UI in world-space Mouse events that bypass the central input gate.

Common control states: normal = ink + edge; hover = raised + text; keyboard focus = 2 px gold outline + 4 px corner ticks; pressed = raised with 1 px content offset while held; selected = gold outline plus persistent short bottom marker; disabled = muted label, dashed/lock cue, no hover brighten or activation; invalid = error outline plus message. Focus and persistent selection are separate: a hovered slot must not change the equipped item or selected hotbar index. Retain focus on Back and restore it after nested views. Keyboard auto-repeat for navigation may start after 300 ms, repeat every 90 ms; confirmation/consume/equip never auto-repeat. UI sounds use existing `snd_ui_move`, `snd_ui_confirm`, `snd_ui_cancel` once per action; use no looping sounds for hover.

## 11. Delivery and implementation acceptance

`UI_LAYOUTS.json` provides machine-readable rectangles, tokens, grid formulas, and source IDs. `UI_ASSETS.csv` distinguishes supplied prototype frame kit, contracted artwork still needed, and optional additions. `UI_QA_CHECKLIST.md` is the engine acceptance checklist. `mockups/*.svg` preserve all layout text as text nodes; their sibling PNGs and `*_annotated.png` are visual references, never full-screen UI textures. The supplied font package includes Regular, Bold, original variable source, and OFL licence. The prototype frame kit is an optional code-generated fallback; portraits/item illustrations remain art-team requests, and their mockup placeholders are explicitly schematic.

Implementation sequence: map design keys to existing state/input/save controllers → configure GUI transform and fonts → health/hotbar → inventory and move transactions → dialogue → save/load and confirmations → pause/settings → death/ending → run the engine checklist. Keep template resources until replacements pass validation. Do not introduce a functioning HTML interface into the game; the SVG/PNG deliverables are specifications only.

Technical references checked for the handoff: fixed GUI coordinates via [GameMaker display_set_gui_size](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Cameras_And_Display/display_set_gui_size.htm); GUI pointer mapping via [device_mouse_x_to_gui](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Game_Input/Device_Input/device_mouse_x_to_gui.htm); font-file pixel sizing via [font_add](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Asset_Management/Fonts/font_add.htm). Noto Sans upstream and licence: [Google Fonts repository](https://github.com/google/fonts/tree/main/ofl/notosans). The specification’s measured pixel layout takes precedence over nominal font point sizes.
