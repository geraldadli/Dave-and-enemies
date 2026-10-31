# Integration report — Dave's & Enemies, Chapter I (Desert)

Engineering report, 31 October 2026. Covers the integration of the UI kit, narrative data, desert_scenes_v2 landscapes, Dave v002 cardinal animations and the 213-file production audio set into one chapter.

**Bottom line.** The chapter is implemented end to end and now **compiles and runs**. Builds are made with Igor using the IDE's own build options file (`Igor.exe -options=<GMS2TEMP>/build.bff -- Windows Compile`); plain command-line Igor still stops at the licence check. A scripted play-test driver (`scr_autotest`, dev-only) played the compiled game from the title through the opening, combat, a chest, a save, a scene pass, death and restore, the Pharaoh fight, defeat, reward, ending and back to the menu. The first real run found and fixed seven bugs (section 7). Human play-testing, listening and balance tuning are still outstanding (section 8).

## 1. Active entry flow and resource IDs

`rm_menu` (title: New Game, Load Game, Settings, Quit) → New Game → `rm_intro` (54 s opening, skip = hold Esc 0.6 s) → `rm_sc_desert_frontier` at cell [7,40] facing east, with the "Travel east through the desert." objective → scene pass at rows 38–42 → `rm_sc_caravan_basin` → scene pass at rows 18–22 → `rm_sc_royal_expanse` → final save star [122,38] → boss throat (row 28 trigger) → Pharaoh courtyard → defeat → dungeon doorway [153..154,12] → ending sequence → `rm_ending` (held title, Return to Main Menu).

The old `rm_d01_arrival` narrative destination is replaced by `rm_sc_desert_frontier` [7,40] through `intro_finish()` (handoff precedence item 2). The template rooms `rm_level_1` and `rm_level_2` remain in the project but are not reachable.

| Scene | Room | Tiles | Save star | Passes |
|---|---|---|---|---|
| Desert Frontier | `rm_sc_desert_frontier` | 128 × 80 | [108,42] | east rows 38–42 ↔ Caravan Basin west |
| Caravan Basin | `rm_sc_caravan_basin` | 144 × 88 | [113,41] | west rows 38–42, east rows 18–22 |
| Royal Expanse | `rm_sc_royal_expanse` | 160 × 96 | [122,38] | west rows 18–22 |

## 2. Implemented systems and changed files

### Code (23 scripts, about 6,400 lines of GML, all new)
| Script | Responsibility |
|---|---|
| `scr_config` | macros (60 Hz, 64 px tiles, 1280×720 GUI, save version 2, 8 + 32 slots), UI colour tokens, mode/overlay enums |
| `scr_util`, `scr_data` | JSON I/O, helpers; loaders/adapters for items, enemies, config, dialogue, narrative manifest (line IDs, portraits, blip profiles), storyboard, scene data, migration map |
| `scr_input` | the single input owner: per-tick polling, fresh-press semantics, consume + block-until-release, GUI-space pointer with letterbox rejection |
| `scr_game` | persistent state machine (base mode + overlay stack, one handler per tick), GUI transform, toasts, new game / restore / load / menu / Game Over flows |
| `scr_ui_kit`, `scr_text`, `scr_ui_screens`, `scr_ui_menus` | nine-slices, buttons, slots, focus/selection, bars, sliders; HUD, inventory, dialogue panel, title, pause, settings, save/load, confirmation, Game Over, ending |
| `scr_inventory`, `scr_stats` | 40-entry storage with equipment references, merge/swap/move, partial loot; XP/levels, derived stats, damage acceptance |
| `scr_save` | settings file, run state, snapshots, atomic slot writes, v1 → v2 migration |
| `scr_world`, `scr_scene` | terrain collision grid, sliding movement, line of sight, spawning from scene data, passes with debounce, barriers, weather, camera |
| `scr_player` | Dave: movement, authored cardinal mapping, data-timed attack, interaction, death |
| `scr_enemy`, `scr_fx` | melee/archer/caster/bat/python/sandworm behaviour, leashes, sleeping, persistence; projectiles, hazards, FX |
| `scr_boss`, `scr_story`, `scr_cinema`, `scr_intro`, `scr_dialogue`, `scr_audio` | Pharaoh arena/AI/defeat/ending; chests, stars, spring, rewards; cinematic control; opening; typewriter + dialogue overlay; audio service |

### Objects
New: `obj_game` (persistent), `obj_enemy`, `obj_pharaoh` (both children of the template `obj_enemy_parent`), `obj_boss_ctrl`, `obj_checkpoint`, `obj_spring`, `obj_pickup`, `obj_prop` and `obj_chest` (children of `obj_collision_parent`), `obj_deco`, `obj_exit`, `obj_gate`, `obj_projectile`, `obj_hazard`, `obj_fx`, `obj_tumbleweed`, `obj_intro`.
Rewritten in GML (template names kept): `obj_player` (now Dave), `obj_manager` (per-room scene bootstrap, depth sort, camera, weather), `obj_menu_manager` (title bootstrap), `obj_chest` (had no events). Their GML Visual event files were replaced. Other template objects are untouched.

### Resources
- Sprites: 13 Dave (9 animations + 4 reference bases), 8 UI frame kit, 7 collision masks (`spr_mask_*`), 8 generated tileset sheets, 45 labelled placeholders (`spr_ph_*`). Template sprites are kept; several serve as documented temps (baddie set, bat, chest, slash).
- Fonts: `fnt_ui_meta` 18 px, `fnt_ui_body` 23 px, `fnt_ui_heading` 28 px Bold, `fnt_ui_dialogue` 28 px, `fnt_ui_title` 46 px Bold, pre-rendered from the supplied Noto Sans TTFs at exact pixel ems (glyph cell = ascent + descent). `OFL.txt` ships in `datafiles/licenses/`.
- Sounds: 213 production takes (see the audio report). The 26 template sounds are kept and no longer triggered by any active object.
- Tilesets: `ts_d_sand/path/grass/water/paving/chasm/bridge/walls` (placeholder textures, generated only for neighbour configurations that occur).
- Rooms: `rm_intro`, `rm_sc_desert_frontier`, `rm_sc_caravan_basin`, `rm_sc_royal_expanse`, `rm_ending` new; `rm_menu` rebuilt (template sequence layer removed, background kept).
- Included Files: `data/items.json`, `enemies.json`, `game_config.json`, `audio_catalog.json`, `scene_migration.json`, `scenes/*.json` (3), the delivered `dialogue.json`, `narrative_manifest.json`, `intro_storyboard.json`, and `licenses/OFL.txt`.
- Project config: `.yyp` resources, folders, Included Files and room order (`rm_menu, rm_intro, rm_sc_desert_frontier, rm_sc_caravan_basin, rm_sc_royal_expanse, rm_ending, rm_level_1, rm_level_2`). Game options are unchanged (60 fps, keep-aspect scaling, filtering on).

### Tools (rebuild the generated content)
`tools/import_deliveries.py` (Dave, UI kit, fonts, audio + audit and catalog), `tools/build_placeholders.py`, `tools/build_world.py` (scene adapter, tilesets, rooms, registration), `tools/write_object_events.py`, `tools/write_enemy_data.py`, `tools/gml_lint.py`, `tools/preview_room.py`, `tools/write_audio_report.py`, `tools/gmyy.py` (.yy writers). Creative tools that were already in `tools/` (scene design, audio rendering, validators) are unchanged.

### Docs
`docs/PROJECT_CONTRACT.md` (scene scope, authored west facing, GUI transform, layers, IDs, runtime conventions; verified/provisional tags kept), `docs/ASSET_REQUESTS.md` (integration status, superseded C5, left-facing IDs, bat name collision), `docs/audio/AUDIO_INTEGRATION_REPORT.md`, `docs/audio/audio_import_audit.json`, `docs/integration/import_validation.json`, this report.

## 3. Dave animation mapping and acceptance status

| Direction | Walk | Attack | Idle | `image_xscale` |
|---|---|---|---|---|
| 0 east | `spr_dave_walk_side` | `spr_dave_attack_side` | `spr_dave_base_side` (reference base, stand-in) | 1 |
| 2 north | `spr_dave_walk_up` | `spr_dave_attack_up` | `spr_dave_base_up` (stand-in) | 1 |
| 4 west | `spr_dave_walk_left` | `spr_dave_attack_left` | `spr_dave_base_left` (stand-in) | 1 |
| 6 south | `spr_dave_walk_down` | `spr_dave_attack_down` | `spr_dave_idle_down` (8 f, 10 fps) | 1 |
| 1, 7 / 3, 5 diagonals | side / left (documented fallback) | facing from the mouse aim | — | 1 |

- Imported from numbered PNGs only, never strips plus frames. Validation before import passed for all 9 animations (80 frames) and 4 bases: exact canvases, RGBA, fully transparent borders, pixel-identical strip/frame agreement (`docs/integration/import_validation.json`).
- Static registration check (this session): with every frame drawn at its sidecar origin, the lowest opaque row stays within −2…+2 px of the ground point across idle, walk contacts and all eight attack poses for all four facings. Visual check at 3× zoom: `side` faces east, `left` is a separately drawn west view, and the sword stays in the anatomical right hand.
- Runtime: walk 20 fps with footsteps only on moving contacts at frames 2 and 7 (stride scaled to actual ground speed); attack holds `[3,3,3,3,3,4,4,4]` ticks (27 ticks / 450 ms) from `game_config.json`; active frames 2–4 drive the arc hitbox (weapon `reach`/`arc_deg`, aimed at the cursor); the swing cue fires once on entering frame 2; the slash FX (template `spr_sword_attack` until `spr_fx_slash` arrives) lives for the active frames only. Attack and locomotion share the ground point, so the (+16,+24) canvas translation needs no code offset.
- **Engine acceptance: pending.** `verified_engine_ready` stays false until the IDE checks (native-scale preview, transitions, foot sliding against 4 px/tick, north follow-through with the slash) are done. No stride, hair, cape or outline issue was found in the static checks; none is claimed fixed.

## 4. Bindings and deliberate deviations

**UI.** Rectangles, tokens, fonts and behaviour follow `UI_SPEC.md` / `UI_LAYOUTS.json`: HP group plus exactly 8 hotbar slots; boss bar only during the active encounter; inventory with 32 storage slots plus the 8 main slots at unchanged coordinates (40 entries, equipment as references, merge/swap/cancel without loss, partial pickups that leave the exact remainder); dialogue panel with left portraits, 28 px text, two rows per page, reveal-then-advance on separate presses, hotbar hidden with no hit areas; save/load with three cards, empty/occupied/unusable/busy/success/failure states, overwrite and unsaved-progress confirmations that start on Cancel; pause hierarchy; settings for music, SFX, dialogue blips, reduced flash, screen shake and window mode, saved immediately to `settings.json`; Game Over with Restart Chapter when no checkpoint exists; ending held until a fresh menu input. The GUI uses one logical-to-window transform for drawing, clipping and pointer tests, rejects clicks in the bars, and re-evaluates on window changes.

Deviations:
1. Reveal speed and sentence pause follow the narrative manifest (24 characters/s, 240 ms) rather than UI_SPEC (30 characters/s, 220 ms); the handoff makes narrative timing authoritative.
2. The boss bar fill is drawn in code in the boss colour, because the supplied `spr_ui_hp_fill` is already red and multiplying it by purple would darken it.
3. The title screen shows the game name as text over the template background instead of the template "Hero's Trail" logo; `spr_title_logo` / `spr_title_bg` are still requested (F8).
4. Timed cinematics (intro, defeat, ending) use hold-Escape skip and Escape never opens pause there; the boss dialogue keeps UI_SPEC's Escape → pause → Skip scene.

**Narrative.** `dialogue.json` text is never rewritten; lines resolve by scene ID and zero-based index, expose manifest line IDs, portraits (expression variant, then base portrait, then `spr_ph_portrait_*`) and blip profiles. Normal end, final advance and skip share one idempotent routine per scene: `intro_finish`, `boss_intro_complete`, `boss_defeat_complete`, `boss_ending_finish`. Flags: `intro_seen`, `boss_intro_seen`, `boss_pharaoh_defeated`, `grail_recovered` (always false), `chapter_1_complete`, `ending_seen`, `desert_arrival_seen`. Objectives show as silent toasts (3.5 s / 2.5 s / 3.5 s). The Grail is never shown; the ankh is a valuable, not the Grail.

**Maps.** Terrain and core placements come from the scene JSON; the gameplay sidecar supplies stable enemy IDs and leashes, chest interaction cells, checkpoint safe/quiet rects, scripts, barriers, arrivals, transitions, boss geometry and weather suppression; decorations are separate, non-colliding objects. The adapter cross-checks enemy placements between core JSON and sidecar at build time. Collision uses the terrain grid (`# M` block everything, `~ C x` block walking, bridges walkable), prop/chest base footprints and closed barriers, never art. Passes need a deliberate outward crossing, arrive two cells inside facing inward, pause damage, destroy projectiles, and re-arm only after Dave leaves the arrival corridor and releases the outward key. Enemies sleep beyond 1,500 px without losing state and never leave their leash rect. `python tools/validate_desert_scenes.py` passes 829 checks.

**Audio.** See `docs/audio/AUDIO_INTEGRATION_REPORT.md` (213/213 files, 98 IDs, routes, budgets, ducking, loops, music transitions, discrepancies).

## 5. Save format, migration and consistency

- Format version 2: `save_N.json` = `{version, chapter, saved_at, location, run}`, where `run` is the complete snapshot (scene room, position, facing, checkpoint, location, HP, level, XP, the 40 inventory entries, equipment indices, defeated spawn IDs, remaining chest contents, unique-reward states, flags, cosmetic seed, playtime, objective).
- Writes: temp file → read back and validated → old file renamed to `.bak` → temp renamed into place; any failure restores or keeps the previous file and shows "Save failed. Your previous save is unchanged. Try again." Success text and `snd_save` follow only a successful commit. A save heals Dave and records the star's respawn cell.
- Death restores the whole last snapshot (loaded or saved this session); with no save it restarts from the initial snapshot made on arrival at [7,40]. Nothing auto-saves; cutscenes never write a slot.
- Migration: version 1 (legacy room-chain IDs) migrates only when its checkpoint maps through `scene_migration.json`; chest and reward identities move with it, enemy spawn IDs stay as they are, and the original file is kept as `save_N.json.v1.json`. Anything else is shown as "Cannot load this save" with a reason and left untouched. No version 1 saves exist yet, because the old room chain was never shipped.
- Boss: `boss_pharaoh_defeated` and the pending reward `rm_sc_royal_expanse:u1` are written together during the whiteout, before any claim. The ankh appears at [134,19]; a full inventory leaves it pending and visible. An undefeated snapshot recreates an idle, retryable encounter (the intro plays again on each attempt); a defeated snapshot recreates the cleared courtyard with both barriers open and the reward pending or claimed, and replays no cue.

## 6. Placeholder art still needed

| Requested ID(s) | Affects | Current stand-in |
|---|---|---|
| `spr_dave_*_down_side`, `*_up_side` (+ left-handed), idle side/left/up, `spr_dave_hurt_*`, `spr_dave_death`, `spr_dave_potion` | diagonals, idles, hurt, death, drinking | horizontal facing, reference bases, white flash, code fade, red aura |
| `spr_undead_*`, `spr_skeleton_warrior_*`, `spr_skeleton_archer_*`, `spr_bandit_*`, `spr_bandit_caster_*` | five humanoid families | template baddie set, tinted and scaled per family |
| `spr_bat_fly` (64×64), `spr_bat_dive`, `spr_bat_defeat` | bats | template bat at 0.5 scale (name collision noted in ASSET_REQUESTS) |
| `spr_python_*`, `spr_sandworm_*` | python, sandworm | `spr_ph_python_*`, `spr_ph_sandworm_*` |
| `spr_pharaoh_*`, laser/thunder/summon FX (F1–F4) | boss and telegraphs | `spr_ph_pharaoh_idle/cast`, code-drawn beam, markers, bolts, cracks, dissolve |
| `spr_gate_arena`, `spr_door_sealed`, `spr_dungeon_entrance` | arena gate, east seal, doorway | code-drawn gate and seal, `spr_ph_dungeon_entrance` |
| `tex_*` (A5, C1), `ts_stairs`, `ts_bridge` | all terrain | procedural `ts_d_*` tilesets |
| Props C4, `spr_healing_spring`, `spr_tumbleweed` | landmarks, obstacles, weather | `spr_ph_*` |
| `spr_chest_desert`, `spr_checkpoint_star`, `spr_fx_*` | chests, stars, FX | template chest ×1.6, `spr_ph_checkpoint_star`, code-drawn FX |
| `spr_icon_<id>` ×14 | inventory | `spr_ph_icon_*` (a potion source image exists in `art/source/icons/` but no export was delivered) |
| `spr_portrait_dave`, `spr_portrait_pharaoh` (+ moods) | dialogue | labelled `spr_ph_portrait_*` |
| `spr_intro_*`, `spr_dave_wind_idle_down`, `spr_dave_turn` | opening | `spr_ph_intro_wall/rubble/fallen`, code sky and banner, idle/base art |
| `spr_ending_bg`, `spr_title_bg`, `spr_title_logo` | ending, title | `spr_ph_ending_bg`, template menu background |

Each slot looks up the contract ID first, so importing a validated delivery under that ID replaces the stand-in without code changes.

## 7. Checks executed (commands and results)

| Check | Command / method | Result | Evidence |
|---|---|---|---|
| Delivery validation and import | `python tools/import_deliveries.py` | Dave 13/13, UI 8/8, fonts 5/5, audio 213/213 (98 IDs), 0 rejects | `docs/integration/import_validation.json`, `docs/audio/audio_import_audit.json` |
| Dave ground registration (static) | composite at sidecar origins, this session | within ±2 px for all facings and actions | visual sheet inspected |
| Scene design validator | `python tools/validate_desert_scenes.py` | PASS, 829 checks, 0 errors | console |
| Scene adapter cross-check | `python tools/build_world.py` | core vs sidecar enemy placements identical (boss excluded) | build assertion |
| Tile output | `python tools/preview_room.py …` | Frontier lookout, Basin bridges, Royal arena render correctly from room tile data | preview images inspected |
| GML static lint | `python tools/gml_lint.py` | 111 files, 366 script functions: 0 errors in project code; 2 errors in an unregistered template leftover (`obj_baddie/Collision_obj_collision.gml`); 3 false-positive ternary warnings | console |
| Resource load and link | Igor `-- Windows PackageZip` | "GMSC serialisation: SUCCESSFUL LOAD AND LINK" | console |
| Compilation | `Igor.exe -options=<IDE build.bff> -- Windows Compile` | **passes** (plain Igor without the IDE's options still reports the licence error) | console |
| Scripted play-test, opening | `scr_autotest` plan: title → New Game → opening → hold-Esc skip | arrival `rm_sc_desert_frontier` [7,40] facing east, objective toast, desert music | `AUTOTEST` log + screenshots |
| Scripted play-test, exploration | walk, attack the first undead, open chest c1, save at the oasis star, inventory, pause | undead defeated (XP 12, spawn ID persisted), potion ×2 → ×3, "Saved to slot 1. Health restored.", inventory and pause states correct | log + screenshots |
| Scripted play-test, pass and death | walk east through the pass; press back west inside the arrival corridor; die to a bandit | arrives Caravan Basin [2,40]; no bounce-back; Game Over → restore to the save star (or the initial snapshot when no save) with full HP | log |
| Scripted play-test, boss and ending | final star → throat trigger → two lines → combat → forced zero HP → reward → doorway | walk-in to [122,26], gate closes, dialogue, `mus_pharaoh` at combat, capped bats, laser, thunder; defeat with whiteout, `boss_pharaoh_defeated` + pending `rm_sc_royal_expanse:u1` together; ankh claimed; ending 10 s; To Be Continued held; menu | log + screenshots |

## 8. Remaining blockers and unverified checks

**Bugs found by the first compiled runs (all fixed):**
1. `obj_game` was created at depth −16000, the edge of GameMaker's range, and nothing it drew in Draw GUI appeared, so the game looked stuck on the template background. It is now created at −15000.
2. Game Options had `option_remove_unused_assets` on, which stripped 327 assets referenced only by name in data, including all 213 production sounds and the data-driven placeholders. It is now off (required by the data-driven design).
3. Dave's death called `game_over_begin()` every frame, so the Game Over menu never accepted input. It now runs once per death.
4. The opening's full-height dialogue panel covered Dave and the fallen soldiers that the storyboard frames low in shot; cinematic captions now use a compact top band.
5. The boss camera followed Dave only, leaving the Pharaoh off-screen; it now frames both, weighted toward Dave.
6. Both summoned bats could spawn on the same authored cell; summons now use distinct cells.
7. Thunder warning markers were too faint to read quickly; they now have a stronger fill, outline and "!".

**Dev-only test driver.** `scripts/scr_autotest` is inert unless a file named `autotest.json` sits next to the game data (never in a normal install). It feeds scripted input through the normal input owner, so tests need no window focus, and saves screenshots with `screen_save`.

**Still needs a human (not covered by the scripted runs):**
- [x] Compiles; title → New Game → opening → Desert Frontier [7,40] facing east with the objective toast (scripted run). [ ] Full 54 s watched by a person; skip at the first fade and the final fade.
- [ ] Dave: four authored facings, no mirroring, diagonals fall back cleanly, idle/walk/attack transitions without a ground jump, footsteps on f2/f7 only while moving, 27-tick attack with the hitbox on frames 2–4, no foot sliding at 4 px/tick.
- [ ] UI_QA_CHECKLIST: text clipping, two-row pagination, long descriptions, every interaction state, exactly 8 + 32 slots, full inventory and loot overflow, stack/swap/cancel, equipment references, hidden hotbar has no hitboxes, no click-through, release gating, Escape affects only the top state, keyboard/mouse parity, windowed/fullscreen and 1600×900 / 1920×1080 / 3440×1440 letterboxing with bar clicks rejected.
- [ ] Saves: three independent slots, overwrite defaults to Cancel, unsaved-progress prompt, failure path (read-only save folder), settings unaffected by loading, full snapshot rollback on death, initial fallback.
- [ ] Landscapes: collision masks against cliffs, water, chasm and bridges; both stair loops; reciprocal passes without ping-pong; star peace; archer/caster line of sight; melee clearance; camera clamping; no enemy or loot reset when crossing places or waking AI.
- [ ] Performance in the 160×96 Royal Expanse with all encounters awake.
- [ ] Boss: unavoidable throat trigger with the full mask; one Pharaoh; 0.75 s grace; physical barriers; thunder safe strip reachable at 4 px/tick; caps of two bats and two undead; laser and thunder never overlap; zero-HP shutdown; defeat 7.5 s (normal and reduced flash); skip during gate close, each line, the whiteout and the ending; full-inventory ankh; retry after death; pre-boss save; completed-boss load; ending replay; Pharaoh HP (1,400) against the 3–5 minute target.
- [ ] Audio: everything in the audio report's IDE checklist, including the five-repeat loop auditions and a listening pass on the cue-sheet gains.
