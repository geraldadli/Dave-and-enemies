# UI acceptance checklist

Design review dated 31 October 2026. The generated QA report covers static geometry, font measurements, sample wrapping, exported image formats, and contrast. Boxes below require **Claude’s GameMaker IDE/runtime checks**; they are not marked passed by rendering mockups.

## Contract and content

- [ ] GUI is 1280 × 720 logical pixels; camera size and room scroll do not move the GUI.
- [ ] Preserve all contracted sprite/item/speaker/room IDs; map `ui.*` design keys to runtime names without renaming existing resources.
- [ ] Exactly 8 main entries + 32 extra entries = 40 item-storage entries. Equipment references add no hidden capacity or item copies.
- [ ] Font is one OFL family, Noto Sans Regular/Bold; licence ships with the font files. Render 18 / 23 / 28 / 46 px targets at measured sizes.
- [ ] Every label, hint, count, speaker name, item description, button label, and dialogue page is editable text; mockup PNGs are not imported as complete interfaces.
- [ ] Dave and Pharaoh portraits are 512 × 512 RGBA sources, facing right, displayed at 208 × 208 on the left. Schematic mockup portraits are replaced with finished art.

## Clipping and text fit

- [ ] All content remains inside the 24 px outer safe area. No panel covers a Back/confirm control.
- [ ] All 8 hotbar cells and all 4 × 8 storage cells render, including the last row and column; no hidden 41st slot.
- [ ] Check empty, 1, stack limit 9, and future multi-digit counts. Keycaps, item art, `E` badges, and counts remain distinguishable.
- [ ] Check HP `0 / 140`, `1 / 140`, `140 / 140`, and large future values; fill clips at both ends and never exceeds frame.
- [ ] Check XP 0, just before threshold, exactly threshold, level-up, and maximum level; no divide-by-zero or stale denominator.
- [ ] Test long equipment names and an item description of at least 400 characters. Names wrap/ellipsize at 23/18 px; descriptions scroll inside their viewport and do not cover action buttons.
- [ ] Test both exact boss-intro strings at 28 px, plus a 140-character widest-letter test. Measured wrapping produces at most 2 lines per page; page reveal never clips descenders.
- [ ] Narration has no portrait or fake speaker; reclaimed text area uses its own wrapping width.
- [ ] Long save-location name, level 999, long playtime, and longest localized date remain separate. Location ellipsis exposes full value on focus.
- [ ] Disabled reasons and transaction errors fit the footer; use wrapping/pagination or shorten copy without shrinking below 18 px.
- [ ] Missing portrait/icon/font has a deliberate fallback; no missing-glyph square or invalid sprite index is drawn.

## Readability and visual states

- [ ] Check bright sand, dark tomb, storm, and spell-heavy boss backgrounds; opaque panels keep text legible.
- [ ] Body/secondary text reaches 4.5:1 against its actual runtime background; interactive focus outline reaches 3:1. Check after any alpha/tint modifications.
- [ ] Selected, focused, hovered, pressed, empty, disabled, equipped, carrying, and invalid states are visually distinct without relying on color alone.
- [ ] Hover does not silently change the active slot or equipped item; keyboard focus remains visible after mouse navigation.
- [ ] Low health is readable without rapid flashing; damage trail never conceals actual HP.
- [ ] Normal gameplay shows HP and 8 slots only. XP, level, capacity, stats, and equipment remain in inventory.
- [ ] Temporary failed-action feedback expires; repeated events do not create overlapping toast stacks.
- [ ] Reduced flash replaces the white peak with a slow dark transition while preserving boss cleanup; shake-off removes only camera shake.

## Scaling

- [ ] Native 1280 × 720 at 100% display scale: body and metadata readable without blur.
- [ ] 1600 × 900 (1.25×), 1920 × 1080 (1.5×), 2560 × 1440 (2×): no unequal axis scaling, clipped edges, or blurry font reuse.
- [ ] 1280 × 800: 40 px top/bottom letterbox. 3440 × 1440: 440 px side bars. Controls and pointer hits align at all four content corners.
- [ ] Windowed/fullscreen toggle and Windows DPI 125/150/200% keep the same logical layout and correct pointer mapping.
- [ ] Clicking a letterbox/pillarbox bar never selects an item or attacks.
- [ ] On smaller-than-supported display, proportionally fit as documented and record the readability limit; do not reflow storage into a different capacity.
- [ ] Camera shake, zoom, room transitions, application-surface recreation, and alt-tab do not offset the GUI or leave stale clip state.
- [ ] Nine-slice corners stay 24 px for panels, 16 for buttons, 8 for HP caps; straight alpha has no dark fringe. Icon art stays centered at 48 px.

## Input ownership and inventory safety

- [ ] In gameplay, clicking a hotbar slot selects it and never also attacks. Q consumes exactly one valid potion; full HP consumes none.
- [ ] I/Tab and right-click hotbar open the same inventory. Inventory pauses damage/projectiles/timers and playtime.
- [ ] Inventory click inspects only; Enter performs the labeled action. All controls have keyboard routes; F6 reaches equipment, description, actions, and Close.
- [ ] Inventory Tab closes, while Tab traverses ordinary menus. No ambiguous context with inherited key handlers.
- [ ] Grid arrows and 1–8 do not move Dave or use items. Wheel over a description scrolls text; it does not also select a hotbar slot.
- [ ] Whole-stack move works with mouse and keyboard; same-type merge respects stack limit; swap is atomic; remainder returns to source.
- [ ] Cancel move, close inventory while carrying, start death, and change room never drop, delete, duplicate, or orphan an equipped item.
- [ ] Full inventory with a partial compatible stack is distinguished from completely full. Rejected or remaining loot stays available.
- [ ] All buttons use press/release semantics. Hold attack/Q/Enter while opening and closing each modal; no click-through attack, double use, or skipped page occurs.
- [ ] Hidden hotbar during dialogue has no hitboxes, number shortcuts, wheel changes, Q action, or tooltip. I/Tab during dialogue does not queue an inventory open.
- [ ] First dialogue press reveals; second advances. A held input cannot do both. Blips stop on instant reveal, pause, skip, and scene end.
- [ ] Pause over dialogue, enter Settings, then return: correct page and typewriter timing resume, with combat still blocked.
- [ ] Completing/skipping the introduction initializes gate, music, one-shot flags, boss HP, and combat exactly once.
- [ ] Escape affects only the topmost state: cancel carry → close inventory; leave settings → pause; cancel confirmation → caller. No event activates two layers.

## Save/load, pause, and terminal screens

- [ ] Three slots remain independent after saving, quitting, and restarting. Displayed metadata belongs to the selected slot.
- [ ] Empty save slot accepts Save; empty/corrupt/incompatible slot cannot Load and explains why without deleting data.
- [ ] Overwrite defaults to Cancel; opening Enter cannot also confirm. Escape/right-click cancels; outside-click is inert.
- [ ] Load from an active session confirms loss of unsaved progress. Back restores caller and focus; no accidental resume.
- [ ] Busy Save/Load locks activation until completion; errors remain readable. Failed save preserves previous data when transactional guarantees apply.
- [ ] Save at checkpoint restores HP only after success; ordinary pause Save is disabled with a reason.
- [ ] Settings sliders and toggles work through keyboard and mouse, persist independently, and do not reset on opening a new save.
- [ ] All disabled controls resist Enter, Space, click, shortcut, and wheel activation; reason is accessible.
- [ ] Game Over returns to snapshot; no snapshot uses Restart Chapter. Load is disabled with no valid saves. No death autosave overwrites progress.
- [ ] Boss defeat/whiteout blocks damage and UI input; all summons/projectiles/hazards disappear before control resumes. Boss bar remains absent after fade-in.
- [ ] Dungeon threshold reaches `rm_ending`; ending shows To Be Continued with one Main Menu action, no recovered Grail, no false save claim, no dungeon gameplay.

## Sign-off record

Build/runtime: __________  Display/DPI: __________  Input devices: __________

Reviewer/date: __________  Failing cases and screenshots: __________
