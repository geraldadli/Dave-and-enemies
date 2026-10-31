# PROJECT_CONTRACT — Dave's & Enemies, Chapter I (Desert)

Owner of this file: Claude (engineering/integration). Creative partner: ChatGPT.
Status tags: **[V]** = verified in the project files/tools. **[P]** = provisional (proposed by engineering; change only by agreement).

## 1. Engine and compatibility
- [V] GameMaker LTS 2026: IDE 2026.0.0.16, runtime 2026.0.0.23, VM target, Windows. Game speed 60 fps.
- [V] Base template: YoYo "Hero's Trail" GML Visual sandbox. New code is GML (structs, methods, `function`). Template DnD events are replaced only where a system is rebuilt.
- [V] Builds compile and run through Igor with explicit project/user/runtime/cache paths, or the IDE's build options file. Reverified 2026-10-31 with the layout rendering fixes: all eight compiled terrain atlases match their source exports; scripted runtime checks cover all three scenes. Plain Igor without the user/runtime context may still fail the licence check.
- [V] Runtime has `font_add`, `sprite_add`, `json_parse`, `audio_sound_loop_start/end`. Data can be loaded from Included Files (`datafiles/`).

## 2. View, style, resolution
- [V] Top-down 3/4 perspective: characters face the camera, walls show front faces.
- [V] Art style: smooth, anti-aliased cartoon art (not pixel art). Dark outlines, soft cel shading, light from the top-left, chunky "chibi" proportions (head about 35–40% of body height). Texture filtering is on (`interpolate_pixels: true`).
- [V] Camera/view 1280×720, viewport 1280×720. Rooms are larger and the camera scrolls.
- [V] GUI plane 1280×720 (UI_SPEC). Implemented with `display_set_gui_maximise(s, s, ox, oy)`, `s = min(W/1280, H/720)`, centred, matching the application surface's keep-aspect letterbox (`option_windows_scale: 0`). The same transform drives drawing, clipping and pointer hit-tests. Art is delivered at native size and never upscaled.
- [V] Tiles: 64×64. Room sizes are multiples of 64.

## 3. Size classes (native pixels)
| Class | Body height | Canvas | Origin (feet / ground point) |
|---|---|---|---|
| Dave: idle, walk, hurt, potion | 76–80 (≈ template knight, 77) | 96×96 | (48, 88) |
| Dave: attack | same body | 128×128 | (64, 112) |
| Dave: death | — | 128×96 | (64, 88) |
| Medium enemy (humanoids) | 70–84 | 128×128 | (64, 112) |
| Bat | ~40 wingspan 56 | 64×64 | (32, 32) centre; engine draws ground shadow |
| Python | ~100 long | 128×96 | (64, 72) |
| Sandworm | 128–160 | 192×192 | (96, 176) |
| Pharaoh (boss) | ~140 | 192×192 | (96, 176) (ground point under the floating body) |
| Props | per item (ASSET_REQUESTS) | — | base centre of footprint |
- [P] Origin = ground contact point for every character and prop. This replaces the template's centre origins because attack canvases are larger than locomotion canvases and everything must align on the feet. Template sprites used as placeholders get a per-sprite draw offset in data.
- [P] All frames of one character use one canvas size per class, with the body at the same place in every frame (no per-frame cropping).
- [P] No baked ground shadows: the engine draws a shared soft shadow ellipse.

## 4. Directions
- [V] Movement: 8 directions. Dave's cardinal facings are authored separately, including west: east 0 → `*_side`, north 2 → `*_up`, west 4 → `*_left`, south 6 → `*_down`, all with `image_xscale = 1` (user direction 2026-10-31; replaces the earlier plan to mirror Dave). Mirroring Dave would reverse his right-handed sword and the screen-space light, so it is not used.
- [P] Dave's diagonals and his non-down idles are not delivered yet. Until they are, diagonal movement keeps the horizontal facing (`side` or `left`) and idle side/left/up show the delivered reference bases.
- [P] Other characters (placeholders and enemies) may still mirror their `side` art for left, as in the template.
- [V] Template naming already uses `down` / `side` / `up` with flip for left; the two diagonals extend that convention.
- [P] Medium enemies: `down`, `side`, `up` only (template baddie coverage). Bats and the sandworm face the camera only; the python has `down`, `side`, `up`; the Pharaoh faces `down`.
- [P] Engine direction index (for data): 0=E, 1=NE, 2=N, 3=NW, 4=W, 5=SW, 6=S, 7=SE (GameMaker angle, counter-clockwise from east). Map: 0,4→`side`; 1,3→`up_side`; 2→`up`; 5,7→`down_side`; 6→`down`.

## 5. Animation naming, frames, timing
Naming: `spr_<entity>_<anim>[_<dir>]`, e.g. `spr_dave_walk_down_side`, `spr_undead_attack_up`.
| Anim | Frames | Playback | Loop |
|---|---|---|---|
| idle | 8 | 10 fps | loop |
| walk | 10 | 20 fps | loop. Feet contact on frames 2 and 7 (template convention [V], broadcast message `step`) |
| attack (Dave) | 8 | engine-timed (below) | once |
| hurt | 2–3 | 12 fps | once |
| death/defeat | 8–10 | 10–12 fps | once, holds last frame |
| enemy attack | 8 | engine-timed from data | once |
| fly (bat) | 6 | 15 fps | loop |
| FX | 4–8 | 20–30 fps | once unless noted |
- [P] Dave attack timing (60 fps game frames): frames 0–1 anticipation (3 each), **frames 2–4 active** (3 each, blade sweeping), frames 5–7 recovery (4 each). Total 27 frames (0.45 s). The sword is in the right hand and sweeps right-to-left across the facing direction.
- [P] Active frames are identified by frame index in data (`active: [2, 4]`), never by sprite fps. The hitbox is a code-defined arc (radius and angle per weapon) aimed at the mouse. The slash FX is visible only during active frames.
- [P] Enemy attacks: `windup`, `active` and `recovery` frame ranges are given per enemy in data. Ranged attackers give a **release frame** plus a spawn-point offset per direction (pixels from origin) in the sidecar JSON.

## 6. Collision conventions
- [V] Template solids are children of `obj_collision_parent`. `obj_editor_wall` is an invisible 64×64 block, scaled for runs of cells.
- [P] Characters collide using dedicated mask sprites (`spr_mask_*`), so the art never affects collision: Dave 28×14 ellipse at the feet; medium 32×16; python 48×16; sandworm 64×28; boss 72×30.
- [P] Props: the collision footprint is the base only (a trunk, a rock base), so characters pass behind tall tops. Creative specs state the footprint in pixels or cells.
- [P] Hurt areas (being hit) are circles around the body centre, from data. Art does not need to supply them.

## 7. Depth and room layers
- [V] Sorting: `obj_manager` End Step sets `depth = -bbox_bottom` for instances (kept).
- [V] Template layer names are kept where they apply. [V] Desert rooms (as generated by `tools/build_world.py`), back to front:
  `Background` 800 (sand colour) · `Tiles_Floor` 700 (base sand) · `Tiles_Path` 650 · `Tiles_Grass` 600 · `Tiles_Water` 550 · `Tiles_Paving` 500 · `Tiles_Chasm` 450 · `Tiles_Bridge` 425 · `Tiles_Walls_Below` 300 (rock and masonry tops with front faces, and stairs, in one tileset) · flat decals at depth 150 · instances sorted by ground point (`depth = -y`) · weather at −11000. `Tiles_Shadows`, `Tiles_Walls_Above` and `Wall_Collisions` are not generated: collision comes from the scene terrain grid at runtime (`# M` block everything, `~ C x` block walking only, bridges walkable), plus prop/chest base footprints and closed barriers.
- [P] Tile index 0 of every tileset is empty (a GameMaker rule). [V] External terrain exports must also regenerate `tilesets/<name>/output_tileset.png` with the exact declared output stride and two-pixel edge extrusion. Updating only the source sprite and `.yy` leaves stale images that the compiler still consumes.

## 8. Stable identifiers
- Rooms [V]: `rm_menu`, `rm_intro`, `rm_sc_desert_frontier` (128×80 tiles), `rm_sc_caravan_basin` (144×88), `rm_sc_royal_expanse` (160×96), `rm_ending`. Design and player language say **scene** for the three landscapes and **place** for districts inside them; only the two scene passes load another room. The earlier `rm_d01…rm_d18` / `rm_o1…rm_o6` scheme is superseded (desert_scenes_v2). Template rooms `rm_level_1/2` stay in the project but are not reachable.
- Initial arrival [V]: `rm_sc_desert_frontier` cell [7,40], facing east. Save stars [V]: Desert Frontier [108,42], Caravan Basin [113,41], Royal Expanse [122,38].
- Entities [P]: `dave`, `undead`, `skeleton_warrior`, `skeleton_archer`, `bandit`, `bandit_caster`, `bat`, `python`, `sandworm`, `pharaoh`.
- Speakers: `narrator`, `dave`, `pharaoh`. Items: lowercase snake_case (`potion_health`).
- Persistent IDs: chest `"<room_id>:c<N>"` (e.g. `rm_sc_desert_frontier:c1`); unique reward `"<room_id>:u<N>"` (Pharaoh's ankh: `rm_sc_royal_expanse:u1`); enemy spawn IDs keep their design strings even where they contain legacy room names (`rm_d02_dune_trail:g1:e1`); flags snake_case (`boss_pharaoh_defeated`, `intro_seen`, `boss_intro_seen`, `grail_recovered`, `chapter_1_complete`, `ending_seen`, `desert_arrival_seen`).
- Assets: `spr_`, `snd_` (SFX), `mus_` (music), `ts_` (tilesets), `spr_icon_<item_id>`, `spr_portrait_<speaker>`, `spr_fx_<name>`, `obj_`, `rm_`, `fnt_`. Template asset names stay unchanged.
- [V] Placeholders never take a contract ID: generated stand-ins are `spr_ph_*`, engineering tilesets `ts_d_*`, masks `spr_mask_*`. The runtime looks up the contract ID first and falls back to the placeholder, so an imported delivery takes over without code changes.
- [V] Audio resources: one resource per delivered take, named after its file (`snd_sword_hit_1` …); the stable event ID (`snd_sword_hit`) is the catalog key. Template `snd_player_defeated` keeps its name; the delivered take is `snd_player_defeated_1`.

## 9. Delivery formats
- **Images:** PNG, 8-bit RGBA, sRGB, straight (non-premultiplied) alpha, transparent background. Deliver either individual frames `<asset>_00.png …` or one horizontal strip `<asset>_stripN.png`. Exact canvas from §3, no trimming, origin as specified. Include the reference sheet you used for consistency.
- **Tiles:** deliver seamless 256×256 **material textures** (they must tile on all edges). Engineering builds the 47-tile edge and corner blends procedurally with irregular noise edges. Fixed pieces (stairs, bridges) are delivered as 64×64-grid sheets.
- **Portraits:** 512×512 PNG, bust framing, facing **right** (toward the text). Drawn at 208×208 in a 1280×720 GUI.
- **Icons:** 64×64 PNG, item centred, 3 px padding, readable at 48 px.
- **Audio:** WAV, PCM 16-bit, 44.1 kHz. SFX mono, peaks ≤ −1 dBFS, silence trimmed. Music stereo, around −16 LUFS integrated. Loops either loop the whole file seamlessly, or supply `loop_start` / `loop_end` (seconds) in a sidecar `<asset>.json`. Voice blips: 50–110 ms, mono, 4 variants per speaker. The engine varies pitch by ±6% and triggers a blip about every second character.
- **Fonts:** one OFL-licensed family (Regular + Bold) as TTF with its licence file. Planned GUI sizes: 23 px UI, 28 px dialogue, 46 px titles, minimum 18 px. Text must stay inside ASCII plus — … ’ “ ” × unless the font is confirmed to have other glyphs.

## 10. Data formats (JSON, UTF-8)
Runtime data goes in `datafiles/data/` (Included Files). [V] Scene layouts (`design/desert/scenes/*.json` + `scene_gameplay_specs.json` + `scene_decorations.json`) are converted by `tools/build_world.py` into GameMaker rooms (tile layers) and a compact runtime adapter `datafiles/data/scenes/<room>.json`; the design files stay the source of truth. Other runtime files: `items.json`, `enemies.json`, `game_config.json`, `audio_catalog.json` (generated from the cue sheet), `scene_migration.json` (copy), plus the delivered `dialogue.json`, `narrative_manifest.json` and `intro_storyboard.json`.
```json
// items.json — array
{"id":"potion_health","name":"Health Potion","type":"consumable|weapon|armor|valuable",
 "icon":"spr_icon_potion_health","stack":9,"value":10,"unique":false,
 "desc":"Restores 30 health.","stats":{"heal":30}}
// weapon stats: {"damage":6,"swing_speed":1.0,"reach":72,"arc_deg":120,"multi_hit":false}
// armor stats:  {"defense":2,"max_hp_bonus":0}
```
```json
// dialogue.json — object keyed by scene id
{"boss_intro":{"lines":[
  {"speaker":"dave","text":"Step aside.","mood":"neutral"},
  {"speaker":"pharaoh","text":"You shall not pass. This desert will be your grave.","mood":"menace"}]}}
// max 140 characters per line entry (two lines at 28 px); narrator has no portrait
```
```json
// rooms/<room_id>.json — one file per room
{"room_id":"rm_d01_arrival","display_name":"Desert Arrival","size_cells":[36,22],
 "terrain":["####################################", "..."],
 "exits":[{"id":"east","side":"E","rows":[9,12],"to":"rm_d02_dune_trail","to_exit":"west"}],
 "objects":[{"type":"enemy","enemy":"undead","cell":[20,8]},
            {"type":"chest","id":"rm_d01_arrival:c1","cell":[12,5],"loot":[["potion_health",2]]},
            {"type":"prop","prop":"cactus_tall","cell":[5,3]},
            {"type":"checkpoint","cell":[18,10]}],
 "music":"mus_desert","weather":{"sandstorm":true,"tumbleweeds":true},"notes":""}
```
Terrain legend (1 char = one 64 px cell; `cell` = [column,row], 0-based from top-left):
`.` sand · `,` dark sand path · `;` grass · `~` water · `#` cliff/rock · `M` masonry wall · `_` paved floor · `^` stairs · `C` chasm · `=` bridge E–W · `|` bridge N–S · `x` broken bridge.
Exits must be walkable openings on the border, at least 3 cells wide. Arrival is 2 cells inside the opening. Keep props and enemies at least 2 cells from openings.

## 11. Constraints for creative work
- Silhouettes must read against both pale sand and dark ruins (outline plus value contrast).
- Telegraphs (windups, sandworm warnings, thunder markers, laser aim) must be readable at 1280×720 within ~0.25 s of starting.
- Flashes: no full-screen strobing. Whiteouts are slow fades, and a reduced-flash setting exists.
- The Grail is never shown recovered in Chapter I.
- Placeholders stay in place until a deliverable passes validation (size, alpha, alignment, direction order, timing, loop points). Mismatches are reported with the smallest correction needed.

## 12. Runtime conventions ([V] as implemented 2026-10-31; compile and play-test pending in the IDE)
- One input owner: `obj_game` polls devices once per tick (Begin Step) and routes the tick to the topmost state only (transition > confirmation > child menu > pause > dialogue > inventory > gameplay). Opening, closing or finishing any state consumes the press and blocks held keys until they are released.
- World simulation runs only in plain gameplay (no overlay, transition or in-scene cinematic). Gameplay objects advance their own timers and animation frames, so pausing stops them cleanly; cinematic owners keep animating.
- Saves: `save_1.json` … `save_3.json` (format version 2, one complete snapshot each), written to a temporary file, read back, then swapped in; the previous file survives a failed write. Settings live in `settings.json`, never in a slot. Version 1 (legacy room-chain IDs) migrates through `scene_migration.json` only when its checkpoint maps to a new save star; the original is kept as `save_N.json.v1.json`.
- Dave's attack: frame holds `[3,3,3,3,3,4,4,4]` ticks (27 ticks / 450 ms), active frames 2–4, swing cue on entering frame 2, hit arc aimed at the mouse from weapon `reach` and `arc_deg`, one hit per swing and target.
- Audio: every cue goes through the shared service (`scr_audio`) with per-ID gain, cooldown, limits and priority from `audio_catalog.json`, the shared budgets (SFX 24, warnings 6, movement 6, projectile travel 4, weather 1, dialogue 1, music 1, or 2 during a crossfade), owned idempotent loops and text/warning ducking.
